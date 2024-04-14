TYPST_CONFIG = """
#set raw(theme: "bw.tmTheme")
#let print(
    task_id: "",
    team: "",
    location: "",
    filename: "",
    lang: "",
    filepath: "",
    header: "",
    body
) = {
    set document(author: (team), title: filename)
    set text(font: "ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace", lang: "zh")
    set page(
        paper: "a4",
        header: [
            filename: #filename
            #h(1fr)
            id: #task_id
            #h(1fr)
            Page #counter(page).display("1 of 1", both: true)
        ],
        margin: (
            top: 48pt,
            bottom: 28pt,
            left: 24pt,
            right: 32pt,
        )
    )

    header
    raw(read(filepath), lang: lang)
    body
}

#show raw.line: it => {
    box(stack(
        dir: ltr,
        box(width: 24pt)[#it.number],
        it.body,
    ))
}

#show: print.with(
    task_id: "%s",
    team: "%s",
    location: "%s",
    filename: "%s",
    lang: "%s",
    filepath: "%s",
    header: "%s",
)
"""
