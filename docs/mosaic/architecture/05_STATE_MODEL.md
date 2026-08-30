# Interface State Model

The MVP needs only a small number of states.

## `idle`
No active scenario. The panel shows the general introduction.

## `previewing`
A scenario is hovered, keyboard-focused, or selected on mobile. The panel displays its data.

## `locked` (optional on desktop)
A lightweight click could pin a preview without navigating, but this is not recommended for the desktop MVP: click should remain a clear link action.

## `navigating`
The click opens the scenario page.

## Mobile

`idle → selected → open`

The first tap selects; the **Read scenario** button opens the page.

## Accessibility

Keyboard `focus` must trigger the same visual and informational state as hover.
