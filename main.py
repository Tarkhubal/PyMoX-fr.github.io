import bisect


import bisect


def get_block_prefix(i: int, tag: str = "Stable") -> str:
    if tag == "Unreleased":
        thresholds = [0, 1, 6, 11]
        labels = ["???+ warning", "???+ success", "???+ info", "???+ note", "??? note"]
    else:
        thresholds = [0, 5, 10]
        labels = ["???+ success", "???+ info", "???+ note", "??? note"]
    return labels[bisect.bisect_left(thresholds, i)]


if __name__ == "__main__":
    
    cas='Unreleased'
    # cas=''
    print (cas)
    for i in range(16):
        print(i, get_block_prefix(i, cas))
