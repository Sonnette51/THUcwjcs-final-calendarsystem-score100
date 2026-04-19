a=input().split()
st=[-1]
for i in a:
    if i.isdigit():
        st.append(i)
    else:
        b=int(st.pop())
        a=int(st.pop())
        if i=="+":
            st.append(a+b)
        elif i=="-":
            st.append(a-b)
        elif i=="*":
            st.append(a*b)
        elif i=="/":
            st.append(int(a/b))
        elif i=="^":
            st.append(a**b)
print(st[-1])