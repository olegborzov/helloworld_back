from deepdiff import DeepDiff


def have_json(should_be, data):
    diff = DeepDiff(should_be, data)
    if 'dictionary_item_added' in diff:
        del diff['dictionary_item_added']
    if 'iterable_item_added' in diff:
        del diff['iterable_item_added']

    return diff
