# Grid2D Escape Room Example

This example runs the 2D virtual world in `maps/grid_escape_room.txt`.

```text
#############
#A..#......K#
#.#.#.#####.#
#.#.........#
#.#########D#
#..........G#
#############
```

Goal: find the key (`K`), unlock the locked door (`D`), and reach the goal (`G`).

Run it with:

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_api_key_here
python main.py --model gpt-5-mini --max-steps 40
```

The program prints each step to the terminal and saves a full JSON episode log under `logs/`.
