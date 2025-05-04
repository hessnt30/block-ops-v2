from flask import Flask, jsonify, request
import os
import subprocess
import time
import re

app = Flask(__name__)

@app.route('/server/check/health', methods=['GET'])
def spark_healthreport():
    try:
        # Send the "spark healthreport" command to the tmux session
        subprocess.run(["tmux", "send-keys", "-t", "minecraft", "spark healthreport", "Enter"])

        # Capture the tmux session's output
        result = subprocess.run(["tmux", "capture-pane", "-t", "minecraft", "-p"], stdout=subprocess.PIPE, text=True)
        output = result.stdout

        # Extract relevant sections from the output
        report = {}
        lines = output.split("\n")

        for i, line in enumerate(lines):
            if "CPU usage from last" in line:
                # Extract the "process" line
                process_line = lines[i + 2]
                # Extract the percentage from the process line
                process_percentage = process_line.split(',')[0].strip().replace('%', '')
                report['cpu_usage'] = int(process_percentage)

            elif "Memory usage:" in line:
                # Extract the memory usage percentage
                memory_line = lines[i + 1].strip()
                memory_percentage = memory_line.split('(')[1].split('%')[0].strip()
                report['memory_usage'] = int(memory_percentage)

        return jsonify({"healthreport": report}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Start the Minecraft server
@app.route('/server/action/start', methods=['POST'])
def start_server():
    try:
        # Start the server in a tmux session
        subprocess.Popen(["tmux", "new-session", "-d", "-s", "minecraft", "./start.sh"], cwd="/home/hittermcgee/Desktop/paper-1.21.4")
        return jsonify({"message": "Server starting..."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/server/action/stop', methods=['POST'])
def stop_server():
    try:
        # Check if the tmux session exists
        session_check = subprocess.run(
            ["tmux", "has-session", "-t", "minecraft"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if session_check.returncode != 0:
            return jsonify({"status": "Server is not running."}), 400

        # Send the stop command to the server
        subprocess.run(["tmux", "send-keys", "-t", "minecraft", "stop", "ENTER"])

        # Wait for the server to shut down (optional, replace 5 with a suitable timeout if needed)
        time.sleep(5)

        # Kill the tmux session
        subprocess.run(["tmux", "kill-session", "-t", "minecraft"])

        return jsonify({"status": "Server stopped successfully."})
    except Exception as e:
        return jsonify({"status": "Failed to stop server.", "error": str(e)}), 500

# Check server status
@app.route('/server/check/status', methods=['GET'])
def server_status():
    try:
        result = subprocess.run(["tmux", "has-session", "-t", "minecraft"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return jsonify({"status": "running"}), 200
        else:
            return jsonify({"status": "stopped"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/server/check/player-list', methods=['GET'])
def player_list():
    try:
        # Send the "list" command to the Minecraft server tmux session
        subprocess.run(["tmux", "send-keys", "-t", "minecraft", "list", "ENTER"])

        # Capture the tmux pane output
        result = subprocess.run(["tmux", "capture-pane", "-t", "minecraft", "-p"], stdout=subprocess.PIPE, text=True)
        output = result.stdout.strip()  # Clean up whitespace

        # Log the raw output for debugging
        print(f"Captured output: {output}")

        # Split the output into lines and reverse for recent entries
        lines = output.splitlines()[::-1]  # Process lines from the most recent

        # Find the most recent "list" response
        player_info_line = None
        for line in lines:
            if "players online" in line:
                player_info_line = line.strip()
                break

        if not player_info_line:
            # If no relevant line is found, return empty response
            return jsonify({"players": {"max_players": 0, "num_players_online": 0, "player_names": []}}), 200

        # Parse the line into counts and player names
        parts = player_info_line.split(":")
        if len(parts) < 2:
            # No player names provided
            return jsonify({"players": {"max_players": 0, "num_players_online": 0, "player_names": []}}), 200

        # Extract counts and player names
        count_part = parts[0]
        names_part = parts[1].strip()

        # Parse counts
        count_words = count_part.split()
        num_players_online = int(count_words[2])  # "There are X ..."
        max_players = int(count_words[6])  # "... of a max of Y ..."

        # Parse player names
        player_names = [name.strip() for name in names_part.split(",")] if names_part else []

        # Create response
        response = {
            "players": {
                "num_players_online": num_players_online,
                "max_players": max_players,
                "player_names": player_names,
            }
        }

        return jsonify(response), 200

    except Exception as e:
        # Catch all exceptions and return error details
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
