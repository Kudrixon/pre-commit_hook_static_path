import ast


class Call(NamedTuple):
    name: str
    line: int
    column: int


class Visitor(ast.NodeVisitor):
    def __init__(
            self,
            ignore: Sequence[str] | None = None,
            allow_dict_kwargs: bool = True,
    ) -> None:
        self.builtin_type_calls: list[Call] = []
        self.ignore = set(ignore) if ignore else set()
        self.allow_dict_kwargs = allow_dict_kwargs

    def _check_dict_call(self, node: ast.Call) -> bool:
        return self.allow_dict_kwargs and bool(node.keywords)

    def visit_Call(self, node: ast.Call) -> None:
        if not isinstance(node.func, ast.Name):
            # Ignore functions that are object attributes (`foo.bar()`).
            # Assume that if the user calls `builtins.list()`, they know what
            # they're doing.
            return
        if node.func.id not in set(BUILTIN_TYPES).difference(self.ignore):
            return
        if node.func.id == 'dict' and self._check_dict_call(node):
            return
        elif node.args:
            return
        self.builtin_type_calls.append(
            Call(node.func.id, node.lineno, node.col_offset),
        )


def check_file(
        filename: str,
        ignore: Sequence[str] | None = None,
        allow_dict_kwargs: bool = True,
) -> list[Call]:
    with open(filename, 'rb') as f:
        tree = ast.parse(f.read(), filename=filename)
    visitor = Visitor(ignore=ignore, allow_dict_kwargs=allow_dict_kwargs)
    visitor.visit(tree)
    return visitor.builtin_type_calls
