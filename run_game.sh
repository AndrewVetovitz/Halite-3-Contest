#!/bin/sh

NEW="python3 MyBot.v11.py"
PREVIOUS="python3 MyBot.v10.py"
TEST="python3 test.py"

# ./halite --replay-directory replays/ -vvv --width 32 --height 32 "$NEW" "$PREVIOUS"

# ./halite --replay-directory replays/ -vvv --width 32 --height 32 "$NEW" "$PREVIOUS"
# ./halite --replay-directory replays/ -vvv --width 40 --height 40 "$NEW" "$PREVIOUS"
# ./halite --replay-directory replays/ -vvv --width 48 --height 48 "$NEW" "$PREVIOUS"
# ./halite --replay-directory replays/ -vvv --width 56 --height 56 "$NEW" "$PREVIOUS"
./halite --replay-directory replays/ -vvv --width 64 --height 64 "$NEW" "$PREVIOUS" "$PREVIOUS" "$PREVIOUS"

# ./halite --replay-directory replays/ --width 32 --height 32 "$NEW" "$PREVIOUS"
# ./halite --replay-directory replays/ --width 40 --height 40 "$NEW" "$PREVIOUS"
# ./halite --replay-directory replays/ --width 48 --height 48 "$NEW" "$PREVIOUS"
# ./halite --replay-directory replays/ --width 56 --height 56 "$NEW" "$PREVIOUS"
# ./halite --replay-directory replays/ --width 64 --height 64 "$NEW" "$PREVIOUS"
