def triple_to_sentence(h, r, o, attrs=None):
    attrs = attrs or {}
    if r == "include":
        return f"习题 {h} 涉及概念 {o}。"
    if r == "score":
        return f"学习者 {h} 在习题 {o} 上得分为 {attrs.get('score','?')}。"
    if r == "master":
        return f"这位提问的学生在概念 {o} 上的掌握度为 {attrs.get('master','?')}。"
    if r == "difficulty":
        return f"概念 {h} 的难度值为 {o.replace('diff:','')}。"
    if r == "discrimination":
        return f"习题 {h} 的区分度为 {o.replace('disc:','')}。"
    if r == "similar":
        return f"概念 {h} 与概念 {o} 相似。"
    if r == "prerequisite":
        return f"概念 {h} 是概念 {o} 的前置知识。"
    return f"{h} --{r}--> {o}"
