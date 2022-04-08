# Chessboardcoin game
## Game rules
Two people, A, B are in jail. The jailer is giving them a single chance to escape - they must beat the jailer at a game.
The game rules are as follows:
  - Person A will enter the room alone and the jailer will lay 64 coins on a chessboard, one on each square, in any configuration the jailer desires.
  - The jailer will hide a single tiny key under one of the coins. The key is infinitely thin and it will not be possible to determine which coin the key is under based on any kind of physical disturbance caused by the key being under a coin.
  - Person A can now flip exactly one coin on the board then must leave the room. Saying anything or doing anything other than thinking or flipping a coin while in the room is strictly prohibited (maybe some scratch paper and a pencil is allowed for calculations if needed). Any attempts to game the system, leave notes behind, or cheat in any way will result in instant death for both people.
  - Person B will now enter the room and the same rules apply as to person A. Person B must now select the correct coin based solely on the information available to them on the board.
  - If Person B correctly selects the coin the key is hidden under the jailer will release them both. The jailer will not cheat and will respect the rules of the game.
  - Persons A and B will be given as much time as desired prior to the game to talk together and attempt to devise a strategy. However, the jailer will be fully aware of any strategy and can attempt to place the coins in such a way to attempt to defeat the strategy.


## Playing it
See the [notebook](notebook.ipynb) for an explanation of the strategy I came up with and explanation of some naming conventions.

The playable version doesn't actually kill you if you guess wrong you can keep trying since its supposed to be a learning thing.
### Playing single player:
```
git clone git@github.com:ChanceToZoinks/chessboardcoin.git
cd chessboard_coin
pip install -r requirements.txt
python3 chessgame.py -s
```
You can try messing around with `strategy.yaml` if you want to change the bot behavior.

### Playing with another person:
```
git clone git@github.com:ChanceToZoinks/chessboardcoin.git
cd chessboard_coin
pip install -r requirements.txt
python3 chessgame.py
```

You could also maybe mess around in the notebook.

### Commands
|Command|Args|Description|
|:------|:---|:-------------|
|(q)uit || quit the game|
|(g)uess |x y | guess the key is under (x, y)   x is left to right, y is top to bottom|
|(b)oard || show the board|
|(r)egion |region side | apply a mask to the board showing only the region/dual chosen|
|(p)arity |region side | get the parity of the region identified by (region, side)|
|(v)ector || get all 6 regions' paritys as a string e.g. 101100 where (0,0) is the leftmost slot and (5,0) is the rightmost|
|(o)verlap |r0id r0s r1id r1s ... | apply a mask to the board showing only the intersection of an arbitrary number of regions identified by (rNid, rNs)|
|(t)ell || tells you where the key is, multiplayer only|
|(f)lip |x y | flip the coin at (x,y), multiplayer only|


There's also some stuff in here like a book on coding theory and some notes/exercise solutions I left in here since this started as repo for me to keep my notes in while I went through the book to try to find a solution to the problem in it.
