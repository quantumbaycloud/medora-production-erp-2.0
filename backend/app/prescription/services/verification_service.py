import re
from sqlalchemy.orm import Session
from app.medicine.repository import MedicineRepository

class MedicineVerificationService:

    # =========================================================
    # FALLBACK DATABASE
    # =========================================================
    MEDICINE_DATABASE = {
        "augmentin": {"generic": "Amoxicillin + Clavulanic Acid", "strengths": ["375 mg", "625 mg", "1.2 g"]},
        "paracetamol": {"generic": "Paracetamol", "strengths": ["500 mg", "650 mg", "1000 mg"]},
        "azithromycin": {"generic": "Azithromycin", "strengths": ["250 mg", "500 mg"]},
        "amoxicillin": {"generic": "Amoxicillin", "strengths": ["250 mg", "500 mg"]},
        "cetirizine": {"generic": "Cetirizine", "strengths": ["5 mg", "10 mg"]},
        "omeprazole": {"generic": "Omeprazole", "strengths": ["20 mg", "40 mg"]},
        "pantoprazole": {"generic": "Pantoprazole", "strengths": ["20 mg", "40 mg"]},
        "ibuprofen": {"generic": "Ibuprofen", "strengths": ["200 mg", "400 mg", "600 mg"]},
        "diclofenac": {"generic": "Diclofenac", "strengths": ["50 mg", "75 mg"]},
        "metformin": {"generic": "Metformin", "strengths": ["500 mg", "850 mg", "1000 mg"]},
        "atorvastatin": {"generic": "Atorvastatin", "strengths": ["10 mg", "20 mg", "40 mg"]},
    }

    VALID_DOSAGES = {"OD", "BD", "TDS", "QID", "SOS", "HS", "STAT"}

    @staticmethod
    def normalize_medicine_name(name: str) -> str:
        if not name:
            return ""
        name = str(name).lower().strip()
        name = re.sub(r"^(tab|tablet|cap|capsule)\.?\s*", "", name, flags=re.IGNORECASE)
        name = re.sub(r"\s+", " ", name)
        return name.strip()

    @staticmethod
    def find_medicine(db: Session, pharmacy_id: str, name: str):
        normalized_name = MedicineVerificationService.normalize_medicine_name(name)
        if not normalized_name:
            return None

        # 1. Tenant-scoped PostgreSQL Search
        try:
            results = MedicineRepository.search_medicines(
                db=db,
                pharmacy_id=pharmacy_id,
                query=normalized_name
            )

            if results:
                best_result = results[0]
                return {
                    "matchedName": best_result.name,
                    "medicineName": best_result.name,
                    "brandName": None, # or split from best_result.name if required
                    "generic": best_result.generic_name,
                    "manufacturer": best_result.manufacturer,
                    "dosageForm": best_result.category,
                    "strengths": [],
                    "barcode": best_result.barcode,
                    "sku": best_result.sku,
                    "batchNumber": None,
                    "expiryDate": None,
                    "quantityAvailable": None,
                    "mrp": None,
                    "status": "ACTIVE",
                    "source": "DATABASE",
                    "score": 0.95,
                }
        except Exception:
            pass

        # 2. LOCAL FALLBACK
        for medicine_name, data in MedicineVerificationService.MEDICINE_DATABASE.items():
            if normalized_name == medicine_name or medicine_name in normalized_name:
                return {
                    "matchedName": medicine_name,
                    "medicineName": medicine_name,
                    "brandName": None,
                    "generic": data["generic"],
                    "strengths": data["strengths"],
                    "manufacturer": None,
                    "dosageForm": None,
                    "barcode": None,
                    "sku": None,
                    "batchNumber": None,
                    "expiryDate": None,
                    "quantityAvailable": None,
                    "mrp": None,
                    "status": None,
                    "source": "LOCAL_FALLBACK",
                    "score": 0.95,
                }
        return None

    @staticmethod
    def validate_dosage(dosage: str):
        if not dosage:
            return {"valid": False, "message": "Dosage not detected."}
        dosage = str(dosage).strip()
        if re.search(r"\b(?:OD|BD|TDS|QID|SOS|HS|STAT)\b", dosage, re.IGNORECASE):
            return {"valid": True, "message": "Recognized prescription abbreviation."}
        if re.search(r"\b\d+(?:-\d+){2,3}\b", dosage):
            return {"valid": True, "message": "Recognized numeric dosage format."}
        if re.search(r"\d+(?:/\d+)?\s*(?:morning|moming|afternoon|aft|evening|eve|night)", dosage, re.IGNORECASE):
            return {"valid": True, "message": "Recognized dosage timing."}
        return {"valid": False, "message": "Dosage format could not be verified."}

    @staticmethod
    def validate_duration(duration: str):
        if not duration:
            return {"valid": False, "message": "Duration not detected."}
        duration = str(duration).strip()
        if re.search(r"\b\d+\s*(?:day|days|week|weeks|month|months)\b", duration, re.IGNORECASE):
            return {"valid": True, "message": "Recognized duration format."}
        return {"valid": False, "message": "Duration format could not be verified."}

    @staticmethod
    def verify_medicine(db: Session, pharmacy_id: str, medicine: dict):
        name = medicine.get("name")
        dosage = medicine.get("dosage")
        duration = medicine.get("duration")

        database_result = MedicineVerificationService.find_medicine(db, pharmacy_id, name)
        dosage_result = MedicineVerificationService.validate_dosage(dosage)
        duration_result = MedicineVerificationService.validate_duration(duration)

        if database_result:
            medicine_status = "VERIFIED"
            source = database_result.get("source")
            confidence = 0.95 if source == "DATABASE" else 0.90
            generic = database_result.get("generic")
            strengths = database_result.get("strengths", [])
            generic_suggestion = generic
            message = "Medicine found in the database."
        else:
            medicine_status = "NOT_FOUND"
            confidence = 0.30
            generic = None
            strengths = []
            generic_suggestion = None
            source = None
            message = "Medicine was not found in the configured database."

        if not dosage_result["valid"]:
            confidence = min(confidence, 0.60)

        if duration and not duration_result["valid"]:
            confidence = min(confidence, 0.70)

        review_status = "NEEDS_HUMAN_REVIEW" if confidence < 0.85 else "AUTO_VERIFIED"

        return {
            "name": name,
            "status": medicine_status,
            "confidence": round(confidence, 2),
            "reviewStatus": review_status,
            "matchedMedicine": database_result.get("matchedName") if database_result else None,
            "medicineName": database_result.get("medicineName") if database_result else None,
            "brandName": database_result.get("brandName") if database_result else None,
            "generic": generic,
            "strengths": strengths,
            "manufacturer": database_result.get("manufacturer") if database_result else None,
            "dosageForm": database_result.get("dosageForm") if database_result else None,
            "barcode": database_result.get("barcode") if database_result else None,
            "sku": database_result.get("sku") if database_result else None,
            "dosage": dosage,
            "dosageValidation": dosage_result,
            "duration": duration,
            "durationValidation": duration_result,
            "genericSuggestion": generic_suggestion,
            "databaseSource": source,
            "message": message,
        }

    @staticmethod
    def verify_prescription(db: Session, pharmacy_id: str, medicines: list):
        if not medicines:
            return {
                "totalMedicines": 0,
                "verifiedMedicines": 0,
                "unverifiedMedicines": 0,
                "needsHumanReview": 0,
                "medicines": [],
            }

        results = []
        for medicine in medicines:
            result = MedicineVerificationService.verify_medicine(db, pharmacy_id, medicine)
            results.append(result)

        verified_count = sum(1 for r in results if r["status"] == "VERIFIED")
        human_review_count = sum(1 for r in results if r["reviewStatus"] == "NEEDS_HUMAN_REVIEW")

        return {
            "totalMedicines": len(results),
            "verifiedMedicines": verified_count,
            "unverifiedMedicines": len(results) - verified_count,
            "needsHumanReview": human_review_count,
            "medicines": results,
        }

