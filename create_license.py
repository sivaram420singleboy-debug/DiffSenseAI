from server_api.models.license_model import create_license

# 🔥 CREATE LICENSE
res = create_license("LIC-TEST-001", "2026-12-31")

print(res)