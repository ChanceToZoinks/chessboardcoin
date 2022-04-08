#!/usr/bin/env python3
import random
from enum import Enum
import itertools
import shlex
import readline
from typing import Union
import sys
import yaml


class Coin(Enum):
    HEADS = 0
    TAILS = 1

    @staticmethod
    def random_state():
        return Coin[random.choice(Coin._member_names_)]


class Square:
    def __init__(self, x: int, y: int, coin: Coin) -> None:
        self.x = x
        self.y = y
        self.num = 8 * y + x
        self.coin = coin
        self.is_key = False

    def flip_coin(self) -> None:
        self.coin = Coin(~self.coin.value % 2)

    def __str__(self) -> str:
        return f"{self.coin.value}"

    def __repr__(self) -> str:
        return f"Square(x={self.x}, y={self.y}, coin={self.coin.value}, num={self.num}, is_key={self.is_key})"


class Board:
    def __init__(self) -> None:
        self.__generate_board()
        self.__choose_key_square()
        self.__calculate_all_regions()

    def __generate_board(self) -> None:
        _ = []
        for y, x in itertools.product(range(8), range(8)):
            _.append(Square(x, y, Coin.random_state()))
        self.board: list[Square] = _

    def __choose_key_square(self) -> None:
        _ = random.choice(self.board)
        _.is_key = True

    def __show_board(self, board, sq_asnum=False) -> None:
        _ = ""
        for i, r in enumerate(board):
            if sq_asnum:
                _ += f"{str(r.num):^2s} "
            else:
                _ += f"{str(r):^2s} "
            if i % 8 == 7:
                _ += "\n"
        print(_, end="")

    def __get_region(self, board_filter) -> list:
        region = []
        for square in self.board:
            region.append(board_filter(square))
        return region

    def __board_region_mask(self, sq, region_id, side):
        return sq if (sq.num // 2**region_id) % 2 == side else "-"

    def __board_key_sq_mask(self, sq):
        return "k" if sq.is_key else "-"

    def __board_coords_mask(self, sq, x, y):
        return sq if sq.x == x and sq.y == y else "-"

    def __board_sq_num_mask(self, sq):
        return sq.num

    def __try_get_sq_by_coords(self, _x, _y, board=None):
        _ = lambda x: x.x == _x and x.y == _y
        if board:
            sq = next(filter(_, board), None)
        else:
            sq = next(filter(_, self.board), None)
        return sq

    def __calculate_all_regions(self):
        region_dict = {
            0: {0: [], 1: []},
            1: {0: [], 1: []},
            2: {0: [], 1: []},
            3: {0: [], 1: []},
            4: {0: [], 1: []},
            5: {0: [], 1: []},
        }
        for i in range(6):
            _0 = lambda x: self.__board_region_mask(x, i, 0)
            _1 = lambda x: self.__board_region_mask(x, i, 1)
            region0 = self.__get_region(board_filter=_0)
            region1 = self.__get_region(board_filter=_1)
            region_dict[i][0] = region0
            region_dict[i][1] = region1
        self.regions = region_dict

    def __swap_board_sqs(self, swap_idx) -> None:
        for i in range(len(self.board)):
            if (i + 1) % swap_idx == 0 and (i // 8) % swap_idx == 0:
                if i + 8 < len(self.board):  # swap up
                    self.board[i], self.board[i + 8] = self.board[i + 8], self.board[i]
                else:  # swap down
                    self.board[i], self.board[i - 8] = self.board[i - 8], self.board[i]

    def show_board(self, sq_asnum=False) -> None:
        self.__show_board(self.board, sq_asnum)

    def show_region(self, region_id: int, side: int) -> None:
        if not isinstance(region_id, int) or not isinstance(side, int):
            raise TypeError
        if not side in (0, 1):
            raise ValueError
        if region_id > 5 or region_id < 0:
            raise ValueError
        region = self.regions[region_id][side]
        print(f"region{region_id}, parity={self.get_region_parity(region)}")
        self.__show_board(region)

    def get_region_parity(self, region):
        num_heads = 0
        for elem in region:
            if isinstance(elem, Square):
                num_heads += 1 if elem.coin == Coin["HEADS"] else 0
        return num_heads % 2

    def show_region_parity(self, region_id: int, side) -> None:
        if not isinstance(region_id, int) or not isinstance(side, int):
            raise TypeError
        if not side in (0, 1):
            raise ValueError
        if region_id > 5 or region_id < 0:
            raise ValueError
        print(
            f"region{region_id} parity={self.get_region_parity(self.regions[region_id][side])}"
        )

    def show_region_parity_vectors(self) -> None:
        l0 = []
        l1 = []
        for id, region in self.regions.items():
            for side, squares in region.items():
                if side == 0:
                    n = self.get_region_parity(squares)
                    l0.append(str(n))
                if side == 1:
                    n = self.get_region_parity(squares)
                    l1.append(str(n))

        print(f"side0: {''.join(l0)}\nside1: {''.join(l1)}")

    def get_region_overlap(self, regions) -> list:
        overlap = []
        for x in list(zip(*regions)):
            overlap.append(x[0]) if all(
                map(lambda j: j == x[0], x)
            ) else overlap.append("-")
        return overlap

    def show_region_overlap(self, region_params) -> None:
        regions = []
        for (id, side) in region_params:
            regions.append(self.regions[id][side])
        overlap = self.get_region_overlap(regions)
        self.__show_board(overlap)

    def check_if_square_in_region(
        self, square: Square, region_id: int, side: int
    ) -> bool:
        return square in self.regions[region_id][side]

    def check_if_coords_in_region(
        self, x: int, y: int, region_id: int, side: int
    ) -> bool:
        sq = self.__try_get_sq_by_coords(x, y)
        return self.check_if_square_in_region(sq, region_id, side)

    def flip_coin(self, x: int, y: int) -> None:
        sq = self.__try_get_sq_by_coords(x, y)
        if sq:
            sq.flip_coin()

    def guess(self, x: int, y: int) -> bool:
        sq = self.__try_get_sq_by_coords(x, y)
        if sq:
            return sq.is_key
        return False

    def get_key_square(self) -> Union[Square, None]:
        for square in self.board:
            if square.is_key:
                return square

    def show_only_key(self) -> None:
        _ = lambda x: self.__board_key_sq_mask(x)
        r = self.__get_region(board_filter=_)
        self.__show_board(r)

    def show_only_xy(self, x, y) -> None:
        _ = lambda k: self.__board_coords_mask(k, x, y)
        r = self.__get_region(board_filter=_)
        self.__show_board(r)

    def show_board_as_sq_nums(self) -> None:
        self.__show_board(self.board, sq_asnum=True)

    def show_board_as_sq_nums_swapped(self, swap_idx: int) -> None:  # just show dont actually swap
        _ = lambda k: self.__board_sq_num_mask(k)
        r = self.__get_region(board_filter=_)
        for i in range(len(r)):
            if (i + 1) % swap_idx == 0 and (i // 8) % swap_idx == 0:
                if i + 8 < len(r):  # swap up
                    r[i], r[i + 8] = r[i + 8], r[i]
                else:  # swap down
                    r[i], r[i - 8] = r[i - 8], r[i]
        self.__show_board(r)

    def swap_board(self, swap_idx: int) -> None:  # actually swap
        self.__swap_board_sqs(swap_idx)
        self.__calculate_all_regions()
        self.__show_board(self.board, True)


def load_strategy(strat_file: str = "strategy.yaml"):
    with open(strat_file, "r") as f:
        strat = yaml.load(f, Loader=yaml.Loader)
    return strat


def single_player_bot(B: Board):
    print("Single player mode: Flipping for you.")
    strategy = load_strategy()
    sq = B.get_key_square()
    regions = []
    for region_id, strat in strategy["regions"].items():
        r = B.regions[int(region_id)][strat["side"]]
        r_dual = B.regions[int(region_id)][~strat["side"] % 2]
        p = B.get_region_parity(r)
        if B.check_if_square_in_region(sq, int(region_id), strat["side"]):  # type: ignore
            if p != strat["parity"]:
                regions.append(r)
            else:
                regions.append(r_dual)
        else:  # in the dual
            if p != ~strat["parity"] % 2:
                regions.append(r)
            else:
                regions.append(r_dual)
    overlap = B.get_region_overlap(regions)
    sq_to_flip = [x for x in filter(lambda x: isinstance(x, Square), overlap)][0]
    B.flip_coin(sq_to_flip.x, sq_to_flip.y)


def play_game(import_arg=None):
    single_player = False
    try:
        if sys.argv[1] in ("-s", "--single-player"):
            single_player = True
    except:
        if import_arg in ("-s", "--single-player"):
            single_player = True
    B = Board()
    if single_player:
        single_player_bot(B)
    while True:
        try:
            cmd, *args = shlex.split(input("What would you like to do?\n> ").lower())
        except ValueError:
            continue

        if cmd == "q":
            print(f"Square {repr(B.get_key_square())} was the key square.")
            B.show_only_key()
            break
        elif cmd in ("g", "guess"):
            try:
                x, y = args
                if B.guess(int(x), int(y)):
                    print("Correct!")
                    print(f"{repr(B.get_key_square())} was the key square.")
                    B.show_only_key()
                    break
                else:
                    print("Wrong. Guess again?")
            except TypeError:
                print("x and y must be integers")
            except:
                print("'(g)uess x y' to make a guess at position (x,y)")
        elif cmd in ("b", "board", "show board"):
            B.show_board()
        elif cmd in ("p", "parity", "get region parity"):
            try:
                region_id, side = args
                B.show_region_parity(int(region_id), int(side))
            except TypeError:
                print(
                    "region_id must be an integer in [0, 5) and side an integer in [0,1]"
                )
            except:
                print("'get region (p)arity region_id side' to get a region's parity")
        elif cmd in ("r", "region", "show region"):
            try:
                region_id, side = args
                B.show_region(int(region_id), int(side))
            except TypeError:
                print("region_id must be an integer in [0, 5)")
            except ValueError:
                print("region_id must be an integer in [0, 5)")
            except:
                print("'show (r)egion region_id side' to show a region")
        elif cmd in ("f", "flip", "flip a coin") and not single_player:
            try:
                x, y = args
                B.flip_coin(int(x), int(y))
            except TypeError:
                print("x and y must be integers")
            except:
                print("'(f)lip a coin x y' to flip the coin at position (x,y)")
        elif cmd in ("t", "tell me", "key square") and not single_player:
            print(f"{repr(B.get_key_square())} is the key square.")
        elif cmd in ("v", "vector", "region num vector"):
            B.show_region_parity_vectors()
        elif cmd in ("o", "overlap", "show overlap"):
            try:
                _ = [int(e) for e in args]
                B.show_region_overlap(list(zip(_[::2], _[1::2])))
            except:
                print(
                    f"'show (o)verlap r0id r0s r1id r1s ...' to show region overlap. must use integers"
                )
        elif cmd in ("s", "show xy", "show only xy"):
            try:
                x, y = args
                B.show_only_xy(int(x), int(y))
            except:
                print(f"'(s)how only xy x y', x and y must be integers")


if __name__ == "__main__":
    play_game()
