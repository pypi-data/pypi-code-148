import diro
from diro import parse

if __name__ == "__main__":
    d = parse("3D6k1+1*(10+1)*2")
    d.roll()
    print(f"{d}={d.detail_expr()}={d.calc()}")

    d = parse("D100b2")
    d.roll()
    print(f"{d}={d.detail_expr()}={d.calc()}")

    dice = diro.Dice(face=6, count=3, kq=2)
    result = dice.roll()
    print(f"{dice}={result.detail()}={result()}")

    diro = parse("1/0")
    print(diro.calc())
