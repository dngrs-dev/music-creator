if __name__ == "__main__":
    import argparse, json
    from music_generator import generate_music_main

    parser = argparse.ArgumentParser(description="Music Generator CLI")
    parser.add_argument(
        "--config", type=str, help="Path to JSON config file with song parameters"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="music/music_output_cli.wav",
        help="Output WAV file",
    )
    parser.add_argument(
        "--info",
        type=str,
        default="music/music_output_cli.json",
        help="Output info JSON file",
    )
    args = parser.parse_args()

    if args.config:
        with open(args.config, "r") as f:
            params = json.load(f)
    else:
        params = {
            "sections": [
                {
                    "name": "CLI Section",
                    "duration": 8,
                    "tempo": 120,
                    "key": "C",
                    "scale": "major",
                    "instruments": ["__random__"],
                    "drums": ["__random__"],
                    "effects": ["__random__"],
                }
            ]
        }
    print(f"Generating music to {args.output} ...")
    generate_music_main(params, args.output, args.info)
    print(f"Done. Output: {args.output}\nMetadata: {args.info}")
