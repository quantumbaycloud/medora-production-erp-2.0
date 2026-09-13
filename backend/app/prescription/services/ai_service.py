import json
from app.core.config import settings
import re

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class AIService:

    # =====================================================
    # MAIN AI ANALYSIS
    # =====================================================

    @staticmethod
    def analyze_prescription(text: str):

        api_key = settings.llm_api_key
        base_url = settings.llm_base_url
        model = settings.llm_model

        # -------------------------------------------------
        # If LLM configuration is unavailable,
        # use fallback parser.
        # -------------------------------------------------

        if not api_key or OpenAI is None:
            return AIService._fallback_analysis(
                text
            )

        try:

            client = OpenAI(
                api_key=api_key,
                base_url=base_url,
            )

            prompt = f"""
You are a prescription information extraction AI.

Analyze OCR text extracted from a medical prescription.

The OCR may contain:
- printed text
- handwritten text
- OCR spelling mistakes
- medicine names listed in one section
- dosage information listed in another section
- duration information listed separately
- food instructions
- doctor information
- hospital/clinic information
- patient information
- advice
- follow-up dates

IMPORTANT:
Do NOT invent information.

If information is not clearly available, return null.

==================================================
OCR TEXT
==================================================

{text}

==================================================
TASK
==================================================

Extract:

1. Patient name
2. Doctor name
3. Doctor registration number
4. Hospital or clinic
5. Medicines
6. Dosage for each medicine
7. Duration for each medicine
8. Food instruction for each medicine
9. Prescription advice
10. Follow-up date

==================================================
MEDICINE EXTRACTION
==================================================

Medicine lines can look like:

1)TAB.MEDICINE
2CAP.MEDICINE
3) TAB.MEDICINE

Recognize:
- TAB
- TABLET
- CAP
- CAPSULE

OCR mistakes such as:
- Moming = Morning
- Mornlng = Morning
- Aft = Afternoon
- Eve = Evening

must be corrected when the meaning is clear.

==================================================
DOSAGE
==================================================

Recognize all of these:

1-0-1
1-1-1
0-1-1
1-0-0
OD
BD
TDS
QID
SOS
HS

Also recognize timing formats such as:

1 Morning, 1 Night
1 Moming, 1 Night
1 Moming.1.Night
1Moming1Aft,1 Eve1 Night
1/2Moming.1/2Night

Normalize obvious OCR mistakes.

Examples:

"1 Moming,1.Night"
becomes
"1 Morning, 1 Night"

"1Moming1Aft,1 Eve1 Night"
becomes
"1 Morning, 1 Afternoon, 1 Evening, 1 Night"

"1/2Moming.1/2Night"
becomes
"1/2 Morning, 1/2 Night"

==================================================
IMPORTANT MEDICINE MAPPING RULE
==================================================

The prescription may list all medicines first and then list
their dosage, food instruction and duration separately.

For example:

4)TAB.MEDICINE4
3)TAB.MEDICINE3
2CAP.MEDICINE2
1)TAB.MEDICINE1

After Food
1/2 Morning,1/2 Night

After Food
1 Morning,1 Afternoon,1 Evening,1 Night

Before Food
1 Morning,1 Night

Before Food
1 Morning,1 Night

Duration
10 Days
10 Days
10 Days
10 Days

In this situation, map the information according to the
prescription's ordering.

Do NOT assume dosage must immediately follow the medicine name.

==================================================
DURATION
==================================================

Recognize:

5 days
10 days
1 month
2 months
10Days
10 Days

Normalize:

"10Days"

to:

"10 days"

==================================================
FOOD INSTRUCTIONS
==================================================

Recognize:

Before Food
After Food
Before food
After food

Do not put medicine names into foodInstruction.

==================================================
ADVICE
==================================================

Only extract actual medical/prescription advice.

For example:

AVOID OILY AND SPICY FOOD

is advice.

A medicine line such as:

4)TAB.DEMO MEDICINE4

is NOT advice.

==================================================
FOLLOW-UP
==================================================

Extract values such as:

Follow Up:12-05-2020
Follow-up: 12-05-2020

Do not confuse dates with medicine information.

==================================================
PATIENT
==================================================

Extract the patient name only when clearly identifiable.

For example:

ID266-DEMO PATIENTM

may indicate a patient name, but do not blindly extract
single letters such as "M" as the patient name.

If the patient name is unclear, return null.

==================================================
DOCTOR
==================================================

Extract doctor name only when clearly identifiable.

Examples:

Dr. Amit Gupta
Dr.O

If "Dr.O" is OCR text but there is insufficient evidence
that it is a complete doctor name, return null.

==================================================
REGISTRATION NUMBER
==================================================

Extract the registration number only when clearly associated
with the doctor.

Do not treat arbitrary numbers such as:
- phone numbers
- prescription IDs
- dates
- temperature
- blood pressure
- medicine quantities

as registration numbers.

==================================================
HOSPITAL / CLINIC
==================================================

Extract hospital or clinic only when clearly identified.

Examples:

Apollo Hospital
ABC Clinic
XYZ Medical Center

Do NOT treat:

Address:PUNE

as a hospital name.

Do NOT treat:

SAMPLEPRESCRIPTION

as a hospital name unless the OCR clearly indicates that it
is the hospital/clinic name.

==================================================
OTHER OCR TEXT
==================================================

Ignore irrelevant values such as:

Temperature
Blood pressure
Phone numbers
Address
Timing
Prescription printing instructions
Page formatting text
Chart instructions

unless they belong to one of the requested fields.

==================================================
OUTPUT
==================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "patient": null,
    "doctor": null,
    "registrationNumber": null,
    "hospital": null,
    "medicines": [
        {{
            "name": null,
            "dosage": null,
            "duration": null,
            "foodInstruction": null
        }}
    ],
    "advice": null,
    "followUp": null
}}

Rules:

- Never invent information.
- Use null when information is unavailable.
- Correct obvious OCR errors.
- Preserve medicine names as accurately as possible.
- Preserve dosage meaning.
- Normalize obvious OCR errors in dosage.
- Normalize duration formatting.
- Do not put medicine names into advice.
- Do not put address into hospital.
- Do not use a single character as patient name unless clearly identified.
- Return JSON only.
"""

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a medical prescription "
                            "information extraction system. "
                            "Extract only information supported "
                            "by the OCR text. "
                            "Return structured JSON only."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0,
            )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            return AIService._parse_llm_response(
                content
            )

        except Exception as e:

            print(
                "LLM analysis failed: "
                f"{str(e)}"
            )

            return AIService._fallback_analysis(
                text
            )

    # =====================================================
    # PARSE LLM RESPONSE
    # =====================================================

    @staticmethod
    def _parse_llm_response(
        content: str,
    ):

        if not content:
            return {
                "error": "LLM returned empty response."
            }

        content = content.strip()

        # Remove ```json
        content = re.sub(
            r"^```json\s*",
            "",
            content,
            flags=re.IGNORECASE,
        )

        # Remove ```
        content = re.sub(
            r"^```\s*",
            "",
            content,
        )

        content = re.sub(
            r"\s*```$",
            "",
            content,
        )

        content = content.strip()

        try:

            result = json.loads(
                content
            )

            return AIService._normalize_result(
                result
            )

        except json.JSONDecodeError:

            # Try extracting JSON object if the model
            # added unwanted text around it.

            match = re.search(
                r"\{.*\}",
                content,
                re.DOTALL,
            )

            if match:

                try:

                    result = json.loads(
                        match.group(0)
                    )

                    return AIService._normalize_result(
                        result
                    )

                except json.JSONDecodeError:
                    pass

            return {
                "error": (
                    "LLM returned invalid JSON."
                ),
                "rawResponse": content,
            }

    # =====================================================
    # NORMALIZE RESULT
    # =====================================================

    @staticmethod
    def _normalize_result(
        result: dict,
    ):

        if not isinstance(
            result,
            dict,
        ):
            return {
                "error": (
                    "LLM returned an invalid "
                    "JSON structure."
                )
            }

        medicines = result.get(
            "medicines",
            [],
        )

        if not isinstance(
            medicines,
            list,
        ):
            medicines = []

        normalized_medicines = []

        for medicine in medicines:

            if not isinstance(
                medicine,
                dict,
            ):
                continue

            name = medicine.get(
                "name"
            )

            dosage = medicine.get(
                "dosage"
            )

            duration = medicine.get(
                "duration"
            )

            food_instruction = medicine.get(
                "foodInstruction"
            )

            if isinstance(
                name,
                str,
            ):
                name = name.strip()

            if isinstance(
                dosage,
                str,
            ):
                dosage = AIService._normalize_dosage(
                    dosage
                )

            if isinstance(
                duration,
                str,
            ):
                duration = AIService._normalize_duration(
                    duration
                )

            if isinstance(
                food_instruction,
                str,
            ):
                food_instruction = (
                    AIService
                    ._normalize_food_instruction(
                        food_instruction
                    )
                )

            normalized_medicines.append(
                {
                    "name": name,
                    "dosage": dosage,
                    "duration": duration,
                    "foodInstruction": (
                        food_instruction
                    ),
                }
            )

        advice = result.get(
            "advice"
        )

        if isinstance(
            advice,
            str,
        ):

            # Never allow a medicine line to become advice.
            if re.search(
                r"\b(?:TAB|TABLET|CAP|CAPSULE)\b",
                advice,
                re.IGNORECASE,
            ):
                advice = None

            else:
                advice = advice.strip()

        return {
            "patient": result.get(
                "patient"
            ),
            "doctor": result.get(
                "doctor"
            ),
            "registrationNumber": result.get(
                "registrationNumber"
            ),
            "hospital": result.get(
                "hospital"
            ),
            "medicines": normalized_medicines,
            "advice": advice,
            "followUp": result.get(
                "followUp"
            ),
        }

    # =====================================================
    # DOSAGE NORMALIZATION
    # =====================================================

    @staticmethod
    def _normalize_dosage(
        dosage: str,
    ):

        dosage = dosage.strip()

        replacements = {
            "Moming": "Morning",
            "Mornlng": "Morning",
            "moming": "Morning",
            "mornlng": "Morning",
            "Aft": "Afternoon",
            "aft": "Afternoon",
            "Eve": "Evening",
            "eve": "Evening",
        }

        for old, new in replacements.items():

            dosage = re.sub(
                rf"\b{re.escape(old)}\b",
                new,
                dosage,
            )

        # Handle OCR forms such as:
        # 1Moming1Aft1Eve1Night

        dosage = re.sub(
            r"(?i)(\d+(?:/\d+)?)\s*"
            r"(Morning|Afternoon|Evening|Night)",
            r"\1 \2",
            dosage,
        )

        # Add commas where multiple dosage timings
        # have been merged by OCR.

        dosage = re.sub(
            r"(?i)"
            r"(?<=[a-z])"
            r"(?=\d+(?:/\d+)?\s*(?:Morning|Afternoon|Evening|Night))",
            ", ",
            dosage,
        )

        dosage = re.sub(
            r"\s*[,.;]\s*",
            ", ",
            dosage,
        )

        dosage = re.sub(
            r"\s+",
            " ",
            dosage,
        )

        return dosage.strip()

    # =====================================================
    # DURATION NORMALIZATION
    # =====================================================

    @staticmethod
    def _normalize_duration(
        duration: str,
    ):

        duration = duration.strip()

        duration = re.sub(
            r"(?i)(\d+)\s*(days?|months?)",
            lambda match: (
                f"{match.group(1)} "
                f"{match.group(2).lower()}"
            ),
            duration,
        )

        duration = re.sub(
            r"\s+",
            " ",
            duration,
        )

        return duration.strip()

    # =====================================================
    # FOOD INSTRUCTION NORMALIZATION
    # =====================================================

    @staticmethod
    def _normalize_food_instruction(
        instruction: str,
    ):

        instruction = instruction.strip()

        if re.search(
            r"before\s*food",
            instruction,
            re.IGNORECASE,
        ):
            return "Before Food"

        if re.search(
            r"after\s*food",
            instruction,
            re.IGNORECASE,
        ):
            return "After Food"

        return instruction

    # =====================================================
    # FALLBACK ANALYSIS
    # =====================================================

    @staticmethod
    def _fallback_analysis(
        text: str,
    ):

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        medicines = []

        # -------------------------------------------------
        # Find medicine lines
        # -------------------------------------------------

        medicine_lines = []

        for line in lines:

            match = re.search(
                r"\d+\)?\s*"
                r"(?:TAB|TABLET|CAP|CAPSULE)"
                r"\.?\s*(.+)",
                line,
                re.IGNORECASE,
            )

            if match:

                medicine_lines.append(
                    match.group(1).strip()
                )

        # -------------------------------------------------
        # Find dosage lines
        # -------------------------------------------------

        dosage_lines = []

        for line in lines:

            if re.search(
                r"\b(?:OD|BD|TDS|QID|SOS|HS)\b",
                line,
                re.IGNORECASE,
            ):
                dosage_lines.append(
                    AIService._normalize_dosage(
                        line
                    )
                )
                continue

            if re.search(
                r"\d+(?:/\d+)?\s*"
                r"(?:morning|moming|afternoon|aft|"
                r"evening|eve|night)",
                line,
                re.IGNORECASE,
            ):
                dosage_lines.append(
                    AIService._normalize_dosage(
                        line
                    )
                )
                continue

            if re.search(
                r"\b\d+-\d+-\d+\b",
                line,
            ):
                dosage_lines.append(
                    line
                )

        # -------------------------------------------------
        # Find food instructions
        # -------------------------------------------------

        food_lines = []

        for line in lines:

            if re.search(
                r"before\s*food",
                line,
                re.IGNORECASE,
            ):

                food_lines.append(
                    "Before Food"
                )

            elif re.search(
                r"after\s*food",
                line,
                re.IGNORECASE,
            ):

                food_lines.append(
                    "After Food"
                )

        # -------------------------------------------------
        # Find durations
        # -------------------------------------------------

        duration_lines = []

        for line in lines:

            if re.search(
                r"\d+\s*(?:days?|months?)",
                line,
                re.IGNORECASE,
            ):

                duration_lines.append(
                    AIService._normalize_duration(
                        line
                    )
                )

        # -------------------------------------------------
        # Map values by order
        # -------------------------------------------------

        for index, name in enumerate(
            medicine_lines
        ):

            dosage = (
                dosage_lines[index]
                if index < len(dosage_lines)
                else None
            )

            duration = (
                duration_lines[index]
                if index < len(duration_lines)
                else None
            )

            food_instruction = (
                food_lines[index]
                if index < len(food_lines)
                else None
            )

            medicines.append(
                {
                    "name": name,
                    "dosage": dosage,
                    "duration": duration,
                    "foodInstruction": (
                        food_instruction
                    ),
                }
            )

        # -------------------------------------------------
        # Advice
        # -------------------------------------------------

        advice = None

        for line in lines:

            if re.search(
                r"\bavoid\b",
                line,
                re.IGNORECASE,
            ):

                advice = line
                break

        # -------------------------------------------------
        # Follow-up
        # -------------------------------------------------

        follow_up = None

        follow_match = re.search(
            r"follow\s*[-]?\s*up\s*:"
            r"\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
            text,
            re.IGNORECASE,
        )

        if follow_match:

            follow_up = follow_match.group(1)

        return {
            "patient": None,
            "doctor": None,
            "registrationNumber": None,
            "hospital": None,
            "medicines": medicines,
            "advice": advice,
            "followUp": follow_up,
        }