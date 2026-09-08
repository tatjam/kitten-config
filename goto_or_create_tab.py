from typing import List
from kitty.boss import Boss
from kittens.tui.handler import result_handler


def main(args: List[str]) -> None:
    pass


def reorder_tabs(boss: Boss, tm) -> None:
    if not hasattr(boss, "_virtual_slots"):
        return
    active_tab = tm.active_tab
    # Sort physical tab list by virtual slot
    tm.tabs.sort(key=lambda t: boss._virtual_slots.get(t.id, 999))
    if active_tab:
        tm.set_active_tab(active_tab)
    if hasattr(tm, "mark_tab_bar_dirty"):
        tm.mark_tab_bar_dirty()


@result_handler(no_ui=True)
def handle_result(
    args: List[str], answer: str, target_window_id: int, boss: Boss
) -> None:
    if len(args) < 2:
        return

    slot = int(args[1])
    tm = boss.active_tab_manager
    if tm is None or not tm.tabs:
        return

    if not hasattr(boss, "_virtual_slots"):
        boss._virtual_slots = {}

    first_tab = tm.tabs[0]
    if first_tab.id not in boss._virtual_slots:
        boss._virtual_slots[first_tab.id] = 1
        if boss.active_tab == first_tab and not first_tab.title.startswith("[1]"):
            boss.set_tab_title("[1]")

    target_tab = None
    for tab in tm.tabs:
        if boss._virtual_slots.get(tab.id) == slot:
            target_tab = tab
            break

    if target_tab:
        tm.set_active_tab(target_tab)
        if not target_tab.title.startswith(f"[{slot}]"):
            boss.set_tab_title(f"[{slot}]")
    else:
        boss.launch("--type=tab", "--cwd=current")
        new_tab = boss.active_tab
        if new_tab:
            boss._virtual_slots[new_tab.id] = slot
            boss.set_tab_title(f"[{slot}]")

    reorder_tabs(boss, tm)
