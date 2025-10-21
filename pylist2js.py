import json

def pylist_to_js_array(pylist, filename, keys=None):
    """
    Write a JS file with `const data = [...]`.
    If `keys` is a list, only those keys (in that order) are included from each dict.
    """
    out_list = []
    if keys is None:
        out_list = pylist
    else:
        sorted_data = sorted(pylist, key=lambda d: list(d.values())[0], reverse=True)
        for item in sorted_data:
            filtered = {}
            for k in keys:
                if k in item:
                    v = item[k]
                    if isinstance(v, float):
                        v = round(v, 1)  # format floats with one decimal place
                    if k == "ID":
                        v = int(v)  # ensure IDs are integers
                    filtered[k] = v
            out_list.append(filtered)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(out_list, ensure_ascii=False, indent=2))
