# API-Sentinel 🛡️

### Detect API Breaking Changes Before They Break Your Application

API-Sentinel is a developer tool that compares two API versions and automatically detects changes that may break existing clients.

## 🚀 Features

- Compare API Version 1 and Version 2
- Detect breaking changes
- Detect safe/non-breaking changes
- Identify added endpoints
- Identify removed fields
- Calculate a compatibility score
- Generate a clear compatibility report
- Display risk level: LOW / MEDIUM / HIGH
- Suggest fixes for detected breaking changes

## 🛠️ Tech Stack

- Python
- Flask
- HTML
- CSS
- JavaScript
- JSON

## 🔍 How It Works

1. Provide API Version 1
2. Provide API Version 2
3. Click **Analyze API**
4. API-Sentinel compares both versions
5. The system identifies breaking and safe changes
6. A compatibility score and risk level are generated
7. Suggested fixes are displayed

## 📊 Example

The system can detect changes such as:

- Endpoint Added
- Endpoint Removed
- Field Added
- Field Removed
- Field Type Changed
## Purpose
To detect API breaking changes before they affect applications.
## Scope
API Sentinel compares two API versions and identifies breaking and safe changes.
## Author
Banasri Patra

Example:

`/student` in API v1 contains:

```json
{
  "id": "integer",
  "name": "string",
  "age": "integer"
}
