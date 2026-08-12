from __future__ import annotations
import re
from dataclasses import dataclass

from feature_interfaces.web_drivers.enums import CommonAttrs
from feature_interfaces.web_drivers.i_web_element_driver import IWebElementDriver


@dataclass
class SelectorPart:
    tag: str | None = None
    id: str | None = None
    classes: list[str] = None
    attrs: dict[str, str | None] = None

    def __post_init__(self):
        self.classes = self.classes or []
        self.attrs = self.attrs or {}


def _parse_selector(selector: str) -> list[SelectorPart]:
    selector = selector.strip()
    if not selector:
        return []

    parts: list[SelectorPart] = []
    tokens = [token.strip() for token in selector.split() if token.strip()]
    for token in tokens:
        parts.append(_parse_simple_selector(token))
    return parts


def _parse_simple_selector(token: str) -> SelectorPart:
    part = SelectorPart()
    while token:
        if token.startswith("#"):
            match = re.match(r"^#([^\.\[#]+)", token)
            if not match:
                break
            part.id = match.group(1)
            token = token[match.end() :]
            continue

        if token.startswith("."):
            match = re.match(r"^\.([^\.\[#]+)", token)
            if not match:
                break
            part.classes.append(match.group(1))
            token = token[match.end() :]
            continue

        if token.startswith("["):
            match = re.match(r"^\[([^=\]]+)(?:=([\"'][^\"']*[\"']|[^\]]+))?\]", token)
            if not match:
                break
            attr_name = match.group(1).strip()
            raw_value = match.group(2)
            if raw_value is not None:
                raw_value = raw_value.strip()
                if (
                    len(raw_value) >= 2
                    and raw_value[0] in "'\""
                    and raw_value[-1] == raw_value[0]
                ):
                    raw_value = raw_value[1:-1]
            part.attrs[attr_name] = raw_value
            token = token[match.end() :]
            continue

        match = re.match(r"^([a-zA-Z][a-zA-Z0-9_-]*)", token)
        if match:
            part.tag = match.group(1)
            token = token[match.end() :]
            continue

        break

    return part


def _find_attr_enum(attr_name: str) -> CommonAttrs | None:
    for attr in CommonAttrs:
        if attr.value == attr_name:
            return attr
    return None


def _matches_selector_part(element: IWebElementDriver, part: SelectorPart) -> bool:
    if part.tag is not None and element.Tag != part.tag:
        return False

    if part.id is not None:
        if element.get_attr_value(CommonAttrs.ID) != part.id:
            return False

    if part.classes:
        class_value = element.get_attr_value(CommonAttrs.CLASS) or ""
        class_list = [cls for cls in class_value.split() if cls]
        for class_name in part.classes:
            if class_name not in class_list:
                return False

    for attr_name, attr_value in part.attrs.items():
        if attr_name == CommonAttrs.ID.value:
            if element.get_attr_value(CommonAttrs.ID) != attr_value:
                return False
            continue
        if attr_name == CommonAttrs.CLASS.value:
            if not attr_value:
                class_value = element.get_attr_value(CommonAttrs.CLASS)
                if class_value is None:
                    return False
                continue
            class_value = element.get_attr_value(CommonAttrs.CLASS) or ""
            class_list = [cls for cls in class_value.split() if cls]
            if attr_value not in class_list:
                return False
            continue

        common_attr = _find_attr_enum(attr_name)
        if common_attr is None:
            return False

        if attr_value is None:
            if not element.has_attr(common_attr):
                return False
        elif element.get_attr_value(common_attr) != attr_value:
            return False

    return True


def _query_selector_recursive(
    elements: list[IWebElementDriver],
    selector_parts: list[SelectorPart],
    index: int = 0,
) -> list[IWebElementDriver]:
    results: list[IWebElementDriver] = []
    if index >= len(selector_parts):
        return results

    selector_part = selector_parts[index]
    for element in elements:
        if _matches_selector_part(element, selector_part):
            if index == len(selector_parts) - 1:
                results.append(element)
            else:
                results.extend(
                    _query_selector_recursive(
                        element.Children, selector_parts, index + 1
                    )
                )

        if element.Children:
            results.extend(
                _query_selector_recursive(element.Children, selector_parts, index)
            )

    return results


def query_selector_all(
    roots: list[IWebElementDriver],
    selector: str,
) -> list[IWebElementDriver]:
    selector_parts = _parse_selector(selector)
    if not selector_parts:
        return []
    return _query_selector_recursive(roots, selector_parts, 0)


def query_selector(
    roots: list[IWebElementDriver],
    selector: str,
) -> IWebElementDriver | None:
    results = query_selector_all(roots, selector)
    return results[0] if results else None
