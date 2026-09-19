from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def compare_api(v1, v2):
    changes = []

    endpoints_v1 = v1.get("endpoints", {})
    endpoints_v2 = v2.get("endpoints", {})

    # 1. Endpoint removed
    for endpoint in endpoints_v1:
        if endpoint not in endpoints_v2:
            changes.append({
                "type": "breaking",
                "category": "Endpoint Removed",
                "message": f"{endpoint} was removed from API V2.",
                "impact": "Existing clients using this endpoint may fail.",
                "fix": "Keep the endpoint or provide a migration path."
            })

    # 2. Endpoint added
    for endpoint in endpoints_v2:
        if endpoint not in endpoints_v1:
            changes.append({
                "type": "safe",
                "category": "Endpoint Added",
                "message": f"{endpoint} was added in API V2.",
                "impact": "Existing clients are not affected.",
                "fix": "No action required."
            })

    # 3. Compare common endpoints
    for endpoint in endpoints_v1.keys() & endpoints_v2.keys():

        old_data = endpoints_v1[endpoint]
        new_data = endpoints_v2[endpoint]

        old_response = old_data.get("response", {})
        new_response = new_data.get("response", {})

        # 4. Removed fields
        for field in old_response:
            if field not in new_response:
                changes.append({
                    "type": "breaking",
                    "category": "Field Removed",
                    "message": f"Field '{field}' was removed from {endpoint}.",
                    "impact": "Clients expecting this field may fail.",
                    "fix": "Keep the field or provide a migration path."
                })

        # 5. Added fields
        for field in new_response:
            if field not in old_response:
                changes.append({
                    "type": "safe",
                    "category": "Field Added",
                    "message": f"Field '{field}' was added to {endpoint}.",
                    "impact": "Existing clients are generally unaffected.",
                    "fix": "Make sure the new field is optional."
                })

        # 6. Data type changed
        for field in old_response.keys() & new_response.keys():

            old_type = old_response[field]
            new_type = new_response[field]

            if old_type != new_type:
                changes.append({
                    "type": "breaking",
                    "category": "Data Type Changed",
                    "message": (
                        f"Field '{field}' changed from "
                        f"{old_type} to {new_type}."
                    ),
                    "impact": "Clients expecting the old data type may fail.",
                    "fix": "Maintain the old type or introduce a new API version."
                })

        # 7. Required fields
        old_required = set(old_data.get("required", []))
        new_required = set(new_data.get("required", []))

        newly_required = new_required - old_required

        for field in newly_required:
            changes.append({
                "type": "breaking",
                "category": "Field Became Required",
                "message": f"Field '{field}' is now required.",
                "impact": "Old client requests may be rejected.",
                "fix": "Keep the field optional or update existing clients."
            })

        # 8. HTTP method change
        old_method = old_data.get("method", "GET")
        new_method = new_data.get("method", "GET")

        if old_method != new_method:
            changes.append({
                "type": "breaking",
                "category": "HTTP Method Changed",
                "message": (
                    f"{endpoint} changed from "
                    f"{old_method} to {new_method}."
                ),
                "impact": "Existing clients using the old method may fail.",
                "fix": "Maintain the old method or create a new endpoint."
            })

    return changes


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        data = request.get_json()

        api_v1 = data.get("api_v1")
        api_v2 = data.get("api_v2")

        if not api_v1 or not api_v2:
            return jsonify({
                "error": "Both API versions are required."
            }), 400

        changes = compare_api(api_v1, api_v2)

        breaking = [
            c for c in changes
            if c["type"] == "breaking"
        ]

        safe = [
            c for c in changes
            if c["type"] == "safe"
        ]

        total = len(changes)

        if len(breaking) >= 3:
            risk = "CRITICAL"
        elif len(breaking) > 0:
            risk = "HIGH"
        elif total > 0:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        # Compatibility score
        if total == 0:
            score = 100
        else:
            score = max(
                0,
                round(100 - (len(breaking) / total) * 100)
            )

        return jsonify({
            "total_changes": total,
            "breaking_changes": len(breaking),
            "safe_changes": len(safe),
            "risk": risk,
            "score": score,
            "changes": changes
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)