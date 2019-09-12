import difflib

for i in range(17):
    text1_lines = open(f'old/{i}_web.html', 'r', encoding="utf8").readlines()
    text2_lines = open(f'new/{i}_web.html', 'r', encoding="utf8").readlines()

    # d = difflib.Differ()
    # diff = d.compare(text1_lines, text2_lines)
    # print('\n'.join(diff))

    diff = difflib.ndiff(text1_lines, text2_lines)
    delta = [x[2:] for x in diff if x.startswith('- ')]
    print("############################################")
    print(i)
    print(delta)