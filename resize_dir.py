from kittens.tui.handler import result_handler


def main(args):
    pass


@result_handler(no_ui=True)
def handle_result(args, answer, target_window_id, boss):
    direction = args[1]
    amount = int(args[2]) if len(args) > 2 else 3
    tab = boss.active_tab
    w = boss.window_id_map.get(target_window_id)
    if tab is None or w is None:
        return
    nb = tab.current_layout.neighbors_for_window(w, tab.windows)
    horizontal = direction in ("left", "right")
    before, after = ("left", "right") if horizontal else ("top", "bottom")
    has_before = bool(nb.get(before))
    has_after = bool(nb.get(after))
    if direction in ("right", "down"):
        sign = 1 if has_after else (-1 if has_before else 0)
    else:
        sign = 1 if has_before else (-1 if has_after else 0)
    if sign:
        tab.resize_window_by(w.id, sign * amount, horizontal)
