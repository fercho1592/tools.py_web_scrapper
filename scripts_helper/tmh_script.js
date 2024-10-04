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
      const name = ("[" + mainFolder + "]/" +anchor.getInnerHTML()).toUpperCase().replace("!","").replace("?","")
      return (href + " | " + name).replace("\n", "")
    })
  
    console.log(result.join("\n"))
})()
