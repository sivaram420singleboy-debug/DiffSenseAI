from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
def get_db():
    return sqlite3.connect("server_api/database/db.sqlite3")

@app.route("/activate", methods=["POST"])
def activate():
    data = request.json

    key = data.get("LicenseKey")
    machine = data.get("MachineId")

    if not key or not machine:
        return jsonify({"status": "invalid"})

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT LicenseKey, MachineId, IsUsed FROM Licenses WHERE LicenseKey=?", (key,))
    row = cur.fetchone()

    if not row:
        return jsonify({"status": "invalid"})

    db_key, db_machine, is_used = row

    # 🔥 FIRST TIME
    if is_used == 0:
        cur.execute(
            "UPDATE Licenses SET MachineId=?, IsUsed=1 WHERE LicenseKey=?",
            (machine, key)
        )
        conn.commit()
        return jsonify({"status": "activated"})

    # 🔥 SAME PC
    if db_machine == machine:
        return jsonify({"status": "already_activated"})

    # 🔥 OTHER PC
    return jsonify({"status": "used_in_other_pc"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)