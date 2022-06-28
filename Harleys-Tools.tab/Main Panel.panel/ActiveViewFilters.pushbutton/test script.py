
projRGBList, cutRGBList, surForPatList, surBacPatList, cutForPatList, cutBacPatList, transList, halfList, prweList = [],[],[],[],[],[],[],[],[]
prPatList, cutweList, cutPatList, surForList, surBacList, cutForList, cutBacList, elementList, nameList = [],[],[],[],[],[],[],[],[]
visibilitiesList, categories = [],[]

current_view = doc.ActiveView
view_filters = {}

filters = current_view.GetFilters()

elements, elementName, visibilities, listprojRGB, listcutRGB, listtrans, listhalf, listprwe, listprPat, listcutwe = [],[],[],[],[],[],[],[],[],[]
listcutPat, rgbsurForList, rgbsurBacList, rgbCutForList, rgbCutBacList, listSurForPat,listSurBacPat,listCutForPat = [],[],[],[],[],[],[],[],[],[]
listCutBacPat,cats = [],[]

for f in filters:
    #if element:
    #    view_filters[
    #        "%s: %s" % (element.Name, visibilities)
    #    ] = elements

    visibilities.append(current_view.GetFilterVisibility(f))
    element=doc.GetElement(f)
    elements.append(element)
    elementName.append(element.Name)
    catid=[Revit.Elements.Category.ById(c.IntegerValue).Name for c in element.GetCategories()]
    cate = catid if len(catid)>1 else catid[0]
    cats.append(cate)
    filterObject = current_view.GetFilterOverrides(f)
    projCol = filterObject.ProjectionLineColor
    if projCol.IsValid:
        projrgb = DSCore.Color.ByARGB(255, projCol.Red, projCol.Green, projCol.Blue)
    else:
        projrgb = None
    listprojRGB.Add(projrgb)

    cutCol= filterObject.CutLineColor
    if cutCol.IsValid:
        cutrgb = DSCore.Color.ByARGB(255, cutCol.Red, cutCol.Green, cutCol.Blue)
    else:
        cutrgb = None
    listcutRGB.Add(cutrgb)
    listtrans.append(filterObject.Transparency)
    listhalf.append(filterObject.Halftone)
    listprwe.append(filterObject.ProjectionLineWeight)
    listprPat.append(doc.GetElement(filterObject.ProjectionLinePatternId))
    listcutwe.append(filterObject.CutLineWeight)
    listcutPat.append(doc.GetElement(filterObject.CutLinePatternId))

    col = filterObject.SurfaceForegroundPatternColor
    if col.IsValid:
        rgbSurFor = DSCore.Color.ByARGB(255, col.Red, col.Green, col.Blue)
    else:
        rgbSurFor = None
    rgbsurForList.Add(rgbSurFor)

    surBacCol = filterObject.SurfaceBackgroundPatternColor
    if surBacCol.IsValid:
        rgbSurBac = DSCore.Color.ByARGB(255, surBacCol.Red, surBacCol.Green, surBacCol.Blue)
    else:
        rgbSurBac = None
    rgbsurBacList.Add(rgbSurBac)

    cut = filterObject.CutForegroundPatternColor
    if cut.IsValid:
        rgbcut = DSCore.Color.ByARGB(255, cut.Red, cut.Green, cut.Blue)
    else:
        rgbcut = None
    rgbCutForList.Add(rgbcut)

    cutBac = filterObject.CutBackgroundPatternColor
    if cutBac.IsValid:
        rgbCutBac = DSCore.Color.ByARGB(255, cutBac.Red, cutBac.Green, cutBac.Blue)
    else:
        rgbCutBac = None
    rgbCutBacList.Add(rgbCutBac)
    listSurForPat.append(doc.GetElement(filterObject.SurfaceForegroundPatternId))
    listSurBacPat.append(doc.GetElement(filterObject.SurfaceBackgroundPatternId))
    listCutForPat.append(doc.GetElement(filterObject.CutForegroundPatternId))
    listCutBacPat.append(doc.GetElement(filterObject.CutBackgroundPatternId))
		
prPatList.append(listprPat)
projRGBList.Add(listprojRGB)
prweList.append(listprwe)
surForPatList.append(listSurForPat)
surForList.Add(rgbsurForList)
surBacPatList.append(listSurBacPat)
surBacList.Add(rgbsurBacList)

cutPatList.append(listcutPat)
cutweList.append(listcutwe)
cutRGBList.Add(listcutRGB)
cutForPatList.append(listCutForPat)
cutForList.Add(rgbCutForList)
cutBacPatList.append(listCutBacPat)
cutBacList.Add(rgbCutBacList)

transList.Add(listtrans)
halfList.Add(listhalf)
visibilitiesList.append(visibilities)
elementList.append(elements)
nameList.append(elementName)
categories.append(cats)

