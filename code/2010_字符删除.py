s = input()
cut = input().strip()
if cut == "":
    print(s)
else:
    print(s.replace(cut, ""))
