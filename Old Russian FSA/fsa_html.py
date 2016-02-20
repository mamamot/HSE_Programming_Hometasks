# encoding: utf-8


def load_text():
    return '<id=5><P CLASS="western" ALIGN=JUSTIFY STYLE="text-indent: 1.25cm; margin-bottom: 0cm; ' \
           'line-height: 191%; widows: 2; orphans: 2"><FONT FACE="KDRS, serif"><FONT SIZE=4><B>СТАРОБРАЗОВАТЫЙ,' \
           '</B><I>прил. </I><SPAN STYLE="text-transform: uppercase"><I>н</I></SPAN><I>есколько старообразный, ' \
           'кажущийся старше своих лет.</I> Олешка Кириловъ сынъ, голова шолудива, очи прочерны, л#тъ в дватцать, ' \
           'лицомъ старобразоватъ, одутловатъ. Новг.каб.кн., 220. 1594&nbsp;г.</FONT></FONT></P>\n'


def fsa(text):
    buffer = list()
    tag_entered = False
    for n, c in enumerate(text):
        if tag_entered:
            if c is not ">":
                continue
            else:
                if text[n+1] is not "<":
                    tag_entered = False
                continue
        if c is "<":
            tag_entered = True
            print("".join(buffer))
            buffer = list()
            continue
        buffer.append(c)

fsa(load_text())
