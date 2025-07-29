((artistName) =>{
    const contentBody = document.getElementsByClassName("panel-body")[1]
    const elementDiv = contentBody.getElementsByClassName("col-xs-6 col-sm-3 col-md-3 col-lg-2")
    const mainFolder = artistName ?? document.getElementsByName("search[searchText]")[0].value

    
    const arrayEle = []
    for (let index = 0; index < elementDiv.length; index++) {
      arrayEle.push(elementDiv[index]);
    }
    
    result = arrayEle.map((element) => {
      const anchor = element.getElementsByTagName("a")[0]
      const href = anchor.getAttribute("href")
      const labelText = anchor.getHTML().trim()
      const name = ("[" + mainFolder + "]/" + labelText).toUpperCase().replace("!","").replace("?","")
      return {url: href, name: name}
    }).sort((a, b) => a.name.localeCompare(b.name))
    .map((element) => (element.url + " | " + element.name).replace("\n", ""))
  
    console.log(result.join("\n"))
})()