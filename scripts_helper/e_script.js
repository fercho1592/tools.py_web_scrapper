((atistName)=>{
    const getTagsByTagType = (ele, tagType, ignore = "original")=>{
        var rows =ele.getElementsByTagName("tr")
    
        const arrayEle = []
        for (let index = 0; index < rows.length; index++) {
            if(rows[index].childNodes[0].innerHTML == tagType)
                arrayEle.push(rows[index]);
        }

        const tagList = arrayEle[0]?.querySelectorAll(".gt,.gtl") ?? []
    
        const tags = []
        for (let index = 0; index < tagList.length; index++) {
            if(tagList[index].innerHTML !== ignore)
                tags.push(tagList[index].innerHTML);
        }

        return tags
    }

    const rows = document.getElementsByClassName("itg glte")[0].getElementsByClassName("gl4e glname")

    const arrayEle = []
    for (let index = 0; index < rows.length; index++) {
        arrayEle.push(rows[index]);
    }

    const result = arrayEle.map((element)=>{
        const anchor = element.parentElement
        const href = anchor.getAttribute("href")        
        
        const parody = getTagsByTagType(element, "parody:")

        const nameElement = anchor.getElementsByClassName("glink")[0]
        const regex = /\([^)]*\)|\[[^\]]*\]/gm;
        const mangaName = nameElement.innerHTML.replace(regex,"").trim();
        let name = ""
        if(parody[0] === undefined)
            name = "[" + atistName + "]/" + mangaName;
        else
            name  = "[" + atistName + "]/[" + parody[0] + "]/" + mangaName;

        name = name.toUpperCase().replace("|", "-").replace("~", "-").replace("?","").replace("!","")

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