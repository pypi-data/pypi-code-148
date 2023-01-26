from typing import Any, List, Optional


class Ticker:
    def __init__(self, data: dict) -> None:
        columns = list(data.keys())

        self.data = {}

        for column in columns:
            # make the column name friendlier
            new_key = column.lower()\
                .replace(" ", "_")\
                .replace(".", "")

            value = self._parse_value(data[column])

            self.data[new_key] = value

    def _parse_value(self, value: str) -> Any:
        if value == "-":
            return None

        if value.count(",") > 0:
            if value.replace(",", "").isnumeric():
                return int(value.replace(",", ""))
            else:
                return value

        if value.count(".") > 0:
            try:
                return float(value)
            except ValueError:
                try:
                    return float(
                        value
                        .replace("M", "E6")
                        .replace("B", "E9")
                        .replace("T", "E12")
                        .replace("%", "")
                    )
                except:
                    return value

        if value.count("%") > 0:
            return float(value.replace("%", ""))

        return value

    def _item(self):
        return self.data

    def _headers(self):
        return list(self.data.keys())

    def _values(self):
        return list(self.data.values())

    def __getattr__(self, __name: str) -> Any:
        try:
            value = self.data[__name]
            return value

        except KeyError:
            raise ValueError(f"Inexistent attribute `{__name}`")

    def __repr__(self) -> str:
        return str(self.data)


class Tickers:
    def __init__(self, tickers: Optional[List[dict]] = []) -> None:
        self.tickers = []

        for ticker in tickers:
            self.add_ticker(ticker)

    def add_ticker(self, ticker: dict) -> None:
        new_ticker = Ticker(ticker)
        self.tickers.append(new_ticker)

    def add_tickers(self, tickers: List[dict]) -> None:
        for ticker in tickers:
            self.add_ticker(ticker)

    def __getitem__(self, idx: int) -> Ticker:
        if idx < len(self.tickers):
            return self.tickers[idx]
        return None

    def __len__(self):
        return len(self.tickers)

    def __repr__(self) -> str:
        return f"Tickers Bin containing {self.__len__()} tickers"

    def to_csv(self, f: str) -> None:
        headers = ','.join([str(i) for i in self.tickers[0]._headers()])
        rows = [headers]

        for ticker in self.tickers:
            rows.append(
                ",".join(
                    [f'"{str(i)}"' if "," in str(i) \
                        or " " in str(i) else str(i) \
                        for i in ticker._values()
                    ]
                ))

        try:
            writer = open(f, "w")

            for row in rows:
                writer.write(str(row))
                writer.write("\n")

            writer.close()

        except Exception as e:
            raise RuntimeError(f"Could not save tickers to csv... {e}")

    def to_list(self) -> List:
        return [ticker._item() for ticker in self.tickers]