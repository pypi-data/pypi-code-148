import re as regex


class Token:
    """
    A `Token` represents a single unit of code. 
    """

    type: str
    """
    The type of token, such as `keyword` or `class name`. Certain types may only exist in certain languages, such as `preprocessor directive` for `C++`.
    """

    value: str
    """
    The part of the token's match that represents the actual value of the token, such as `public` for a `keyword` token. This differs from `full_match` in that some token types have to check characters around the token to correctly identify it, and those characters are not included in the value of the token itself.
    """

    full_match: regex.Match[str]
    """
    The entire match of the token's regular expression. The exact definition of this varies from implementation to implementation, but in general it refers to the `0` group of the regular expression used to identify the token. 
    """

    start: int
    """The index of the entire code block at which the first letter of this token lies."""

    line_start: int
    """The index on the token's line at which it begins."""

    line_number: int
    """The line number that the token is on."""

    def __init__(self, type: str, value: str, full_match: regex.Match[str], start: int, line_number: int, line_start: int):
        """
        Creates a new `Token`. 

        ### Parameters
            - `type: str`:
                - The type of token, such as `keyword` or `class name`.
            - `value: str`:
                - The value of the token, such as `public`. 
            - `full_match: re.Match`
                - The full group matched by the token's regular expression.
            - `start: int`
                - The index of the first character of this token relative to the entire code snippet.
            - `end: int`
                - The index of the last character of this token relative to the entire code snippet. 
        
        ### Returns
        a new `Token` with the specified attributes.

        """
        self.type = type
        self.value = value
        self.full_match = full_match
        self.start = start
        self.line_number = line_number
        self.line_start = line_start

    def __str__(self):
        return f"Token[ type = {self.type}, value = {repr(self.value)}, start = {self.start}, line_number = {self.line_number}, line_start = {self.line_start} ]"


class TokenIdentifier:

    regex: str
    group: int
    type: str

    def __init__(self, token_type: str, regex: str, group: int = 0):
        self.regex = regex if regex.startswith("^") else f"^{regex}"
        self.type = token_type
        self.group = group
        

class TokenizableLanguage:

    identifiers: list[TokenIdentifier]
    default_identifiers = [
        TokenIdentifier("identifier", r"^[a-z_]\w*\b"),
        TokenIdentifier("left parentheses", r"^\("),
        TokenIdentifier("right parentheses", r"^\)"),
        TokenIdentifier("left brace", r"^\{"),
        TokenIdentifier("right brace", r"^\}"),
        TokenIdentifier("semicolon", r"^;"),
        TokenIdentifier("left bracket", r"^\["),
        TokenIdentifier("right bracket", r"^\]"),
        TokenIdentifier("newline", r"^\n+"),
        TokenIdentifier("number", r"^-?\d+(\.\d+)?"),
        TokenIdentifier("symbol", r"^(=|\+|\-|\*|<|>|/|%|&|\||!|\.|\:)+", 1),
        TokenIdentifier("string", r'^"([^"]|\\")*"'),
        TokenIdentifier("constant", r"^[A-Z_]+\b"),
        TokenIdentifier("class name", r"^[A-Z](\w)*\b"),
        TokenIdentifier("function", r"^([A-Za-z_]\w*)\s*\(", 1),
        TokenIdentifier("whitespace", r"^ +"),
        TokenIdentifier("comment", r"^//[^\n]*"),
        TokenIdentifier("comma", r",")
    ]

    def __init__(self, identifiers: list[TokenIdentifier]):
        """
        Creates a new programming language that can be tokenized. By default, several `TokenIdentifiers` are in place that are common in many languages, such as matching `r"^//[^\\n]*"` for `comment`. Any identifier passed to the `identifiers` parameter with the same name as a default `TokenIdentifier` will override the default in place, such as:

        ```python
        Python = TokenizableLanguage(
            identifiers = [
                TokenIdentifier("comment", r"#[^\\n]*"),
                ...
            ]
        )
        ```

        For a full comprehensive list of default token identifiers, see `default_identifiers`.
        """

        # Empty dictionary
        id_dict: dict[str, TokenIdentifier] = {}

        # Add default identifiers 
        for default_identifier in TokenizableLanguage.default_identifiers:
            id_dict[default_identifier.type] = default_identifier

        # Add and override identifier arguments
        for identifier in identifiers:
            id_dict[identifier.type] = identifier

        # Reverse identifier dictionary so that arguments come first (and thus their regexs have priority)
        self.identifiers = list(id_dict.values())
        self.identifiers.reverse()

        
    def tokenize(self, code: str) -> list[Token]:
        """
        Tokenizes the given code snippet into a `list` of `Tokens` using this `TokenizableLanguage`.
        """
        code = code.replace("\r", "")
        tokens: list[Token] = []
        pos = 0
        line_number = 1
        line_pos = 0
        while(code):
            match_found = False
            for identifier in self.identifiers + TokenizableLanguage.default_identifiers:
                match = regex.match(identifier.regex, code)
                if (match):
                    str_match = match.group(identifier.group)
                    token = Token(
                        type = identifier.type, 
                        value = str_match,
                        full_match = match,
                        start = pos,
                        line_number = line_number,
                        line_start = line_pos
                    )
                    code = code[len(str_match):]
                    pos += len(str_match)
                    tokens.append(token)
                    if token.type == "newline":
                        line_number += len(str_match)
                        line_pos = 0
                    else:
                        line_pos += len(str_match)
                    match_found = True
                    break
            if not match_found: raise Exception("Unrecognized Token: " + code)
        return tokens


# Assembly

C = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while)\b"),
        TokenIdentifier("directive", r'#[a-z]+\s*<.+?>')
    ]
)

Cpp = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(alignas|alignof|and|and_eq|asm|atomic|cancel|atomic|commit|atomic|noexcept|auto|bitand|bitor|bool|break|case|catch|char|char8_t|char16_t|char32_t|class|compl|concept|const|consteval|constexpr|constinit|const_cast|continue|co_await|co_return|co_yield|decltype|default|delete|do|double|dynaimc_cast|else|enum|explicit|export|extern|float|for|friend|goto|if|inline|int|long|mutable|namespace|new|noexcept|not|not_eq|nullptr|operator|or|or_eq|private|protected|public|reflexpr|register|reinterpret_cast|requires|return|short|signed|sizeof|static|static_assert|static_cast|struct|switch|synchronized|template|thread_local|throw|try|typedef|typeid|typename|union|unsigned|using|virtual|void|volatile|wchar_t|while|xor|xor_eq)\b"),
        TokenIdentifier("keyword literal", r"(false|nullptr|this|true)\b")
    ]
)

CSharp = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(abstract|as|base|bool|break|byte|case|catch|char|checked|class|const|continue|decimal|default|delegate|do|double|else|enum|event|explicit|extern|finally|fixed|float|for|foreach|goto|if|implicit|in|int|interface|internal|is|lock|long|namespace|new|object|operator|out|override|params|private|protected|public|readonly|ref|return|sbyte|sealed|short|sizeof|stackalloc|static|string|struct|switch|throw|try|typeof|uint|ulong|unchecked|unsafe|ushort|using|using|static|void|volatile|while)\b"),
        TokenIdentifier("keyword literal", r"(false|null|this|true)\b")
    ]
)

Fortran = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(assign|backspace|block|call|close|common|continue|data|dimension|do|else|if|integer|end|endfile|endif|entry|equivalence|external|format|function|goto|if|implicit|inquire|intrinsic|open|parameter|pause|print|program|read|return|rewind|rewrite|save|stop|subroutine|then|write)\b"),
        TokenIdentifier("comment", r"![^\n]*"),
        TokenIdentifier("symbol", r"((=|\+|\-|\*|<|>|/|%|&|\||!|\.|\:)+|\.[A-Z]+\.)")
    ]
)

Go = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(break|case|chan|const|continue|default|defer|else|fallthrough|for|func|go|goto|if|import|interface|map|package|range|return|select|struct|switch|type|var)\b"),
    ]
)

Haskell = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(case|class|data|default|deriving|do|else|forall|if|import|in|infix|infixl|infixr|instance|let|module|newtype|of|qualified|then|type|where|_|foreign|ccall|as|safe|unsafe`)\b")
    ]
)

Java = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(abstract|assert|boolean|break|byte|case|catch|char|class|continue|default|do|double|else|enum|extends|final|finally|float|for|if|implements|import|instanceof|int|interface|long|native|new|package|public|return|short|static|strictfp|super|switch|synchronized|throw|throws|transient|try|void|volative|while)\b", 1),
        TokenIdentifier("keyword literal", r"(false|null|this|true)\b")
    ]
)

JavaScript = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(as|break|case|catch|class|const|constructor|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|import|in|instanceof|new|let|module|of|return|set|super|static|string|switch|throw|try|var|while|with|yield)\b"),
        TokenIdentifier("keyword literal", r"(false|null|this|true)\b")
    ]
)

Lua = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(and|break|do|else|elseif|end|false|for|function|if|in|local|not|or|repeat|return|then|true|until|while)\b"),
        TokenIdentifier("keyword literal", r"(nil)\b"),
        TokenIdentifier("comment", r"--[^\n]*")
    ]
)

Python = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(and|as|assert|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b"),
        TokenIdentifier("keyword literal", r"(False|None|self|True)\b"),
        TokenIdentifier("comment", r"#[^\n]*"),
    ]
)

Ruby = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(__ENCODING__|__LINE|__FILE__|BEGIN|END|alias|and|begin|break|case|class|def|defined|do|else|elsif|end|ensure|for|if|in|module|next|not|or|redo|rescue|retry|return|super|then|trueundef|unless|until|when|while|yield)\b"),
        TokenIdentifier("keyword literal", r"(false|nil|self|true)\b")
    ]
)

Rust = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(as|async|await|break|consts|continue|crate|dyn|else|enum|extern|fn|for|if|impl|in|let|loop|match|mod|move|mut|pub|ref|return|Self|static|struct|super|trait|type|unsafe|use|where|while)\b"),
        TokenIdentifier("keyword literal", r"(false|self|true)\b")
    ],
)

SQL = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(ADD|ALL|ALTER|AND|ANY|AS|ASC|BACKUP|BETWEEN|CASE|CHECK|COLUMN|CONSTRAINT|CREATE|DATABASE|INDEX|OR|REPLACE|VIEW|TABLE|PROCEDURE|UNIQUE|INDEX|DEFAULT|DELETE|DESC|DISTINCT|DROP|EXEC|EXISTS|FOREIGN|KEY|FROM|FULL|OUTER|JOIN|GROUP|BY|HAVING|IN|INNER|JOIN|INSERT|INTO|SELECT|IS|NULL|NOT|LEFT|LIKE|LIMIT|NOT|OR|ORDER|OUTER|PRIMARY|PROCEDURE|RIGHT|ROWNUM|INTO|TOP|SET|TABLE|TOP|TRUNCATE|UNION|ALL|UPDATE|VALUES|WHERE)\b")
    ]
)

TypeScript = TokenizableLanguage(
    identifiers = [
        TokenIdentifier("keyword", r"(any|as|boolean|break|case|catch|class|const|constructor|continue|debugger|declare|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|new|let|module|number|of|private|protected|public|require|return|set|super|static|string|switch|symbol|throw|try|type|typeof|var|void|while|with|yield)\b"),
        TokenIdentifier("keyword literal", r"(false|null|this|true)\b")
    ]
)

# XML
