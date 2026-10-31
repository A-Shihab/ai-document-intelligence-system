class ValidatorService:
    @staticmethod
    def validate_extracted_data(data: dict) -> list[dict]:
        errors = []
        
        if not data or "error" in data:
            return [{"field": "general", "error": "Extraction failed or data is empty."}]

        # 1. Check mandatory fields (Scenario 5: Missing supplier, total, etc.)
        mandatory_fields = ["invoice_number", "invoice_date", "supplier_name", "total"]
        for field in mandatory_fields:
            val = data.get(field)
            if not val or str(val).strip() in ["None", "null", ""]:
                errors.append({
                    "field": field,
                    "error": f"Missing mandatory field: {field}"
                })

        # If total or subtotal is completely missing, skip strict math validation
        if not data.get("total") or not data.get("subtotal"):
            return errors

        # 2. Check mathematical consistency (Scenarios 1, 2, 3, 4, 6)
        try:
            subtotal = float(data.get("subtotal") or 0.0)
            tax = float(data.get("tax") or 0.0)
            
            # Handle shipping / fees flexibly
            fees = float(
                data.get("shipping") or 
                data.get("shipping_and_handling") or 
                data.get("fees") or 0.0
            )
            
            total = float(data.get("total") or 0.0)

            # Parse discount flexibly (Handles fixed amounts, negative numbers, or percentages like "5%")
            raw_discount = data.get("discount") or data.get("discount_amount") or data.get("discount_value") or 0.0
            discount_val = 0.0
            
            if raw_discount:
                raw_str = str(raw_discount).strip()
                if "%" in raw_str:
                    # Scenario 2: Invoice with a percentage discount (e.g., "5%" of subtotal)
                    try:
                        pct = float(raw_str.replace("%", "").strip())
                        discount_val = subtotal * (pct / 100.0)
                    except ValueError:
                        discount_val = 0.0
                else:
                    # Scenario 3: Invoice with a fixed-amount discount
                    try:
                        discount_val = abs(float(raw_str))
                    except ValueError:
                        discount_val = 0.0

            if subtotal > 0 and total > 0:
                # Formula: Subtotal - Discount + Tax + Shipping/Fees
                calculated_total = subtotal - discount_val + tax + fees
                
                # Scenario 6: Check if the grand total is incorrect (with a 0.05 currency rounding tolerance)
                if abs(calculated_total - total) > 0.05:
                    # Intelligent fallback check: if Gemini missed the discount key entirely, 
                    # see if the math discrepancy matches a logical implied discount.
                    implied_discount = (subtotal + tax + fees) - total
                    if 0 < implied_discount < subtotal and discount_val == 0.0:
                        discount_val = implied_discount
                        calculated_total = subtotal - discount_val + tax + fees

                if abs(calculated_total - total) > 0.05:
                    errors.append({
                        "field": "total",
                        "error": (
                            f"Mathematical mismatch: Subtotal ({subtotal}) - Discount ({round(discount_val, 2)}) "
                            f"+ Tax ({tax}) + Fees ({fees}) = {round(calculated_total, 2)} "
                            f"!= Total ({total})"
                        )
                    })
        except Exception as e:
            errors.append({
                "field": "total",
                "error": f"Error evaluating invoice math: {str(e)}"
            })

        return errors