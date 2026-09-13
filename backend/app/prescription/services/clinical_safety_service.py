from typing import List, Dict, Any

class ClinicalSafetyService:

    INTERACTIONS = {
        frozenset(["ibuprofen", "aspirin"]): {
            "severity": "HIGH",
            "message": "These medicines may increase the risk of gastrointestinal bleeding.",
        },
        frozenset(["warfarin", "ibuprofen"]): {
            "severity": "HIGH",
            "message": "This combination may increase bleeding risk.",
        },
        frozenset(["warfarin", "aspirin"]): {
            "severity": "HIGH",
            "message": "This combination may increase bleeding risk.",
        },
        frozenset(["ibuprofen", "naproxen"]): {
            "severity": "HIGH",
            "message": "Using multiple NSAIDs may increase the risk of gastrointestinal and kidney-related adverse effects.",
        },
        frozenset(["simvastatin", "clarithromycin"]): {
            "severity": "HIGH",
            "message": "This combination may increase simvastatin exposure and adverse effects.",
        },
    }

    MEDICINE_ALLERGY_GROUPS = {
        "amoxicillin": ["penicillin", "amoxicillin", "beta-lactam"],
        "augmentin": ["penicillin", "amoxicillin", "beta-lactam"],
        "ibuprofen": ["ibuprofen", "nsaid", "aspirin"],
        "aspirin": ["aspirin", "nsaid"],
        "diclofenac": ["diclofenac", "nsaid"],
    }

    BRAND_TO_GENERIC = {
        "augmentin": {"generic": "Amoxicillin + Clavulanic Acid", "brand": "Augmentin"},
        "calpol": {"generic": "Paracetamol", "brand": "Calpol"},
        "azithral": {"generic": "Azithromycin", "brand": "Azithral"},
        "crocin": {"generic": "Paracetamol", "brand": "Crocin"},
        "zifi": {"generic": "Cefixime", "brand": "Zifi"},
        "pan": {"generic": "Pantoprazole", "brand": "Pan"},
        "omez": {"generic": "Omeprazole", "brand": "Omez"},
    }

    @staticmethod
    def normalize(name: str) -> str:
        if not name:
            return ""
        name = name.lower().strip()
        for prefix in ["tab ", "tablet ", "cap ", "capsule ", "syp ", "syrup "]:
            if name.startswith(prefix):
                name = name[len(prefix):]
        return name.strip()

    @staticmethod
    def check_drug_interactions(medicines: List[str]) -> Dict[str, Any]:
        normalized = [ClinicalSafetyService.normalize(m) for m in medicines if m]
        interactions = []

        for i in range(len(normalized)):
            for j in range(i + 1, len(normalized)):
                med_a = normalized[i]
                med_b = normalized[j]
                key = frozenset([med_a, med_b])
                match = ClinicalSafetyService.INTERACTIONS.get(key)
                if match:
                    interactions.append({
                        "medicine1": med_a,
                        "medicine2": med_b,
                        "severity": match["severity"],
                        "message": match["message"],
                    })

        return {
            "interaction_found": len(interactions) > 0,
            "interactions": interactions,
            "message": "Potential interaction(s) detected." if interactions else "No interaction found.",
        }

    @staticmethod
    def check_allergies(medicines: List[str], allergies: List[str]) -> Dict[str, Any]:
        norm_meds = [ClinicalSafetyService.normalize(m) for m in medicines if m]
        norm_allergies = [ClinicalSafetyService.normalize(a) for a in allergies if a]
        warnings = []

        for med in norm_meds:
            groups = ClinicalSafetyService.MEDICINE_ALLERGY_GROUPS.get(med, [])
            for allergy in norm_allergies:
                if allergy in groups:
                    warnings.append({
                        "medicine": med,
                        "allergy": allergy,
                        "severity": "HIGH",
                        "message": f"Medicine '{med}' matches allergy group '{allergy}'. Clinical review required.",
                    })

        return {
            "warning_found": len(warnings) > 0,
            "warnings": warnings,
            "message": "Potential allergy warning detected." if warnings else "No configured allergy match found.",
        }

    @staticmethod
    def get_generic_suggestions(medicines: List[str]) -> Dict[str, Any]:
        suggestions = []
        for med in medicines:
            norm = ClinicalSafetyService.normalize(med)
            match = ClinicalSafetyService.BRAND_TO_GENERIC.get(norm)
            if match:
                suggestions.append({
                    "medicine": med,
                    "brand": match["brand"],
                    "generic": match["generic"],
                    "suggestion_available": True,
                    "message": "Generic equivalent found.",
                })
            else:
                suggestions.append({
                    "medicine": med,
                    "brand": None,
                    "generic": None,
                    "suggestion_available": False,
                    "message": "No generic mapping found in database.",
                })

        return {
            "suggestions": suggestions,
            "message": "Generic medicine lookup completed.",
        }
