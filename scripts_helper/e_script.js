((atistName)=>{
    const rows = document.getElementsByClassName("gl3c glname")

    const arrayEle = []
    for (let index = 0; index < rows.length; index++) {
        arrayEle.push(rows[index]);
    }

    const result = arrayEle.map((element)=>{
        const anchor = element.getElementsByTagName("a")[0]
        const href = anchor.getAttribute("href")
        const nameElement = anchor.getElementsByClassName("glink")[0]
        const regex = /\([^)]*\)|\[[^\]]*\]/gm;
        let mangaName = nameElement.innerHTML.replace(regex,"").trim();

        const name = "[" + atistName + "]/" + mangaName;

        return (href + " | " + name).replace("\n", "")
    })

    console.log(result.join("\n"))
})()

((atistName)=>{
    const href = document.URL

    const regex = /\([^)]*\)|\[[^\]]*\]/gm;
    let mangaName = document.getElementById("gn").innerHTML.replace(regex,"").trim();

    const name = "[" + atistName + "]/" + mangaName;

    const result = (href + " | " + name).replace("\n", "")

    console.log(result)
})()