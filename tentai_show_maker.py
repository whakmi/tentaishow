import random
numregions = 0
rcl = []                                        # regional cell list. contains all the cell positions of a given region.         
outgrid = []
sdelimcell = 0
galaxymapticker = 1

def genimage(width, height, outgrid):
    import datetime
    from PIL import Image, ImageDraw
    imgwidth = 50*width + 10
    imgheight = 50*height + 10
    outimg = Image.new(mode="RGB", size=(imgwidth, imgheight))
    draw = ImageDraw.Draw(outimg)
    draw.rectangle((5, 5, (imgwidth-6), (imgheight-6)), fill=(255, 255, 255))
    for i in range(1,width):
        draw.rectangle(((50*i + 4), 5, (50*i + 5), (imgheight - 6)), fill=(219, 219, 219))
    for i in range(1,height):
        draw.rectangle((5, (50*i + 4), (imgwidth - 6), (50*i + 5)), fill=(219, 219, 219))
    cellpointer = 0
    for i in range(0, height):
        for j in range(0, width):
            if outgrid[cellpointer] != ".":
                if str(outgrid[cellpointer]).islower():
                    white = 0
                else:
                    white = 255
                if str(outgrid[cellpointer]).lower() == "c":
                    horizoffset = 0
                    vertoffset = 0
                elif str(outgrid[cellpointer]).lower() == "r":
                    horizoffset = 25
                    vertoffset = 0
                elif str(outgrid[cellpointer]).lower() == "b":
                    horizoffset = 0
                    vertoffset = 25
                else:
                    horizoffset = 25
                    vertoffset = 25
                draw.ellipse(((20 + 50*j + horizoffset), (20 + 50*i + vertoffset), (39 + 50*j + horizoffset), (39 + 50*i + vertoffset)), fill=(white, white, white), outline=(0, 0, 0), width=2)
            cellpointer += 1
    now = datetime.datetime.now()
    output = outimg.save("tentaishow_" + now.strftime("%Y%m%d_%H%M%S") + ".png")

def regionfill(cell):                           # acts like a paint bucket tool for regions dropped at a defined cell
    if outgrid[cell] == "X":
        global numregions
        chkcell = 0
        chkcellcontent = 0
        if regionsgrid[cell] == 0:              # if the cell doesn't already belong to a region, make a new region
            numregions += 1
            regionsgrid[cell] = numregions
        # check for available cell left
        chkcell = cell - 1
        if cell % width != 0:
            chkcellcontent = regionsgrid[chkcell]
            if chkcellcontent == 0 and grid[cell] == grid[chkcell]:
                regionsgrid[chkcell] = regionsgrid[cell]
                regionfill(chkcell)
        # check for available cell right
        chkcell = cell + 1
        if chkcell % width != 0:
            chkcellcontent = regionsgrid[chkcell]
            if chkcellcontent == 0 and grid[cell] == grid[chkcell]:
                regionsgrid[chkcell] = regionsgrid[cell]
                regionfill(chkcell)
        # check for available cell up
        chkcell = cell - width
        if chkcell >= 0:
            chkcellcontent = regionsgrid[chkcell]
            if chkcellcontent == 0 and grid[cell] == grid[chkcell]:
                regionsgrid[chkcell] = regionsgrid[cell]
                regionfill(chkcell)
        # check for available cell down
        chkcell = cell + width
        if chkcell < area:
            chkcellcontent = regionsgrid[chkcell]
            if chkcellcontent == 0 and grid[cell] == grid[chkcell]:
                regionsgrid[chkcell] = regionsgrid[cell]
                regionfill(chkcell)
    return 0

def singledoubleelim():                         # finds all regions of 1 or 2 cells and resolves them accordingly
    global sdelimcell
    global galaxymap
    global galaxymapticker
    regionnumber = 0
    for regionnumber in range(1, numregions+1):
        regionarea = cellsinregion(regionnumber)
        sdelimcell = 0
        # singles elim
        if regionarea == 1:
            while regionnumber != regionsgrid[sdelimcell]:
                sdelimcell += 1
            if grid[sdelimcell] == 0:
                outgrid[sdelimcell] = "c"
            else:
                outgrid[sdelimcell] = "C"
            regionsgrid[sdelimcell] = -1
            galaxymap[sdelimcell] = galaxymapticker
            galaxymapticker += 1
        # doubles elim
        if regionarea == 2:
            while regionnumber != regionsgrid[sdelimcell]:
                sdelimcell += 1
            if regionsgrid[sdelimcell] == regionsgrid[sdelimcell+1] and width != 1:
                regionsgrid[sdelimcell] = -1
                galaxymap[sdelimcell] = galaxymapticker
                regionsgrid[sdelimcell+1] = -1
                galaxymap[sdelimcell+1] = galaxymapticker
                if grid[sdelimcell] == 0:
                    outgrid[sdelimcell] = "r"
                else:
                    outgrid[sdelimcell] = "R"
                outgrid[sdelimcell+1] = "."
            else:
                regionsgrid[sdelimcell] = -1
                galaxymap[sdelimcell] = galaxymapticker
                regionsgrid[sdelimcell+width] = -1
                galaxymap[sdelimcell+width] = galaxymapticker
                if grid[sdelimcell] == 0:
                    outgrid[sdelimcell] = "b"
                else:
                    outgrid[sdelimcell] = "B"
                outgrid[sdelimcell+width] = "."
            galaxymapticker += 1
    return 0

def genreflection(dotlocation, dottype, focuscell):
    tweener = 0
    if dottype == "c":
        reflectioncell = 2 * dotlocation - focuscell           
    elif dottype == "r":
        reflectioncell = 2 * dotlocation - focuscell + 1
        tweener = 0.5
    elif dottype == "b":
        reflectioncell = 2 * dotlocation - focuscell + width
    elif dottype == "d":
        reflectioncell = 2 * dotlocation - focuscell + width + 1
        tweener = 0.5
    if ((dotlocation % width) + tweener) < (focuscell % width):
        if ((dotlocation % width) + tweener) < (reflectioncell % width):
            return -1
    elif ((dotlocation % width) + tweener) > (focuscell % width):
        if ((dotlocation % width) + tweener) > (reflectioncell % width):
            return -1
    if reflectioncell < 0 or reflectioncell >= area:
        return -1
    return reflectioncell

def cellsinregion(targetregion):                # retrieves the number of cells which belong to a given region
    cell = 0
    numcells = 0
    for cell in range(0, area):
            if targetregion == regionsgrid[cell]:
                numcells += 1
    return numcells

def getregionalcells(targetregion):             # stuffs all cells in a specified region into the global list "rcl"
    global rcl
    rcl = []
    cell = 0
    while cell < area:
        if regionsgrid[cell] == targetregion:
            rcl.append(cell)
        cell += 1

def placegalaxy():                              # places a "good" galaxy dot within the current bounds of rcl
    validdotslist = []
    global outgrid
    global galaxymapticker
    global galaxymap
    for focuscell in rcl:
        validdotslist.append(4*focuscell)               # center placements are always valid
        if focuscell+1 < area and (focuscell+1) % width != 0 and regionsgrid[focuscell] == regionsgrid[focuscell+1]:
            validdotslist.append(4*focuscell + 1)       # get "r" placement validity
        if focuscell+width < area and regionsgrid[focuscell] == regionsgrid[focuscell+width]:  
            validdotslist.append(4*focuscell + 2)       # get "b" placement validity
        if (focuscell+1) % width != 0 and focuscell+width+1 < area and regionsgrid[focuscell] == regionsgrid[focuscell+1] and regionsgrid[focuscell] == regionsgrid[focuscell+width] and regionsgrid[focuscell] == regionsgrid[focuscell+width+1]:
            validdotslist.append(4*focuscell + 3)       # get "d" placement validity
    # now that we have scores for all placements, pick some number of candidates at random.
    # the default is 15, but can be increased to optimize for bigger galaxies
    # rewrite everything below this, hehe
    dotcandidates = []
    for i in range(0, 15):
        dotcandidates.append(random.choice(validdotslist))
    # the dot's location is given by integer division by 4, and the type is given by a modulo 4 operation
    winninggalaxycells = []
    for dotcandidate in dotcandidates:
        galaxybuffercells = []                  # the galaxy currently being generated is stored in galaxybuffer
        dotloc = dotcandidate // 4
        galaxybuffercells.append(dotloc)
        if dotcandidate % 4 == 0:
            dottype = "c"
            galaxysize = 1
        elif dotcandidate % 4 == 1:
            dottype = "r"
            galaxybuffercells.append(dotloc+1)
            galaxysize = 2
        elif dotcandidate % 4 == 2:
            dottype = "b"
            galaxybuffercells.append(dotloc+width)
            galaxysize = 2
        else:
            dottype = "d"
            galaxybuffercells.append(dotloc+1)
            galaxybuffercells.append(dotloc+width)
            galaxybuffercells.append(dotloc+width+1)
            galaxysize = 4
        # generate a galaxy for the dotcandidate
        expattempts = 0
        validexpansion = 0
        stopgen = 0
        while stopgen == 0:
            seedcell = random.choice(galaxybuffercells)     # choose a cell to try and expand from
            expanddir = random.randrange(0,4)               # choose a direction to try and expand to (0L, 1R, 2U, 3D)
            if expanddir == 0:                              # these secondary & tertiary "if" lines make sure expandcell is valid
                expandcell = seedcell - 1
                if seedcell % width != 0 and expandcell >= 0:
                    if regionsgrid[expandcell] == regionsgrid[seedcell]:
                        validexpansion = 1
            elif expanddir == 1:
                expandcell = seedcell + 1
                if expandcell % width != 0 and expandcell < width:
                    if regionsgrid[expandcell] == regionsgrid[seedcell]:
                        validexpansion = 1
            elif expanddir == 2:
                expandcell = seedcell - width
                if expandcell >= 0 and seedcell >= width:
                    if regionsgrid[expandcell] == regionsgrid[seedcell]:
                        validexpansion = 1
            else:
                expandcell = seedcell + width
                if expandcell < area:
                    if regionsgrid[expandcell] == regionsgrid[seedcell]:
                        validexpansion = 1
            if expandcell in galaxybuffercells:
                validexpansion = 0                          # don't expand into a cell that the galaxy already owns
            if validexpansion == 1:
                expansionrefl = genreflection(dotloc, dottype, expandcell)
                if expansionrefl == -1:                     # now perform similar checks on the cell opposite the dot
                    validexpansion = 0
                else:
                    if regionsgrid[expansionrefl] != regionsgrid[seedcell] or galaxymap[expansionrefl] != galaxymap[seedcell]:
                        validexpansion = 0
            if expandcell >= area:
                validexpansion = 0
            if validexpansion == 1:
                galaxybuffercells.append(expandcell)
                galaxybuffercells.append(expansionrefl)
                galaxysize = len(galaxybuffercells)
            expattempts += 1
            if galaxysize >= 0.18 * area or expattempts >= 800:
                stopgen = 1
                expattempts = 0
        # if the galaxy we just generated is bigger than the current winning galaxy, it will overwrite the previous one
        if galaxysize > len(winninggalaxycells):
            winninggalaxycells = galaxybuffercells
            winninggalaxyloc = dotloc
            winninggalaxytype = dottype
    # after getting our winning galaxy, put it into effect
    for cell in winninggalaxycells:
        regionsgrid[cell] = -1
        galaxymap[cell] = galaxymapticker
        outgrid[cell] = "."
    galaxymapticker += 1
    if grid[winninggalaxyloc] == 0:
        outgrid[winninggalaxyloc] = winninggalaxytype
    else:
        outgrid[winninggalaxyloc] = winninggalaxytype.capitalize()
    # regenerate regions for whatever region we just punched a hole in
    for cell in rcl:
        if regionsgrid[cell] != -1:
            regionsgrid[cell] = 0
    for cell in rcl:
        if regionsgrid[cell] == 0:
            regionfill(cell)
    return 0

dimensions = "0x0"
while dimensions == "0x0":
    dimensions = input("Input the dimensions of the puzzle (e.g. 15x5): ")
    invalid = 0
    heightswitch = 0
    widthstr = ""
    heightstr = ""
    for char in dimensions:
        if invalid == 0:
            if char.isdigit():
                if heightswitch == 0:
                    widthstr = widthstr + char
                else:
                    heightstr = heightstr + char
            else:
                if char == "x" and heightswitch == 0:
                    heightswitch = 1
                else:
                    dimensions = "0x0"
                    print("Invalid format.")
                    invalid = 1
    if widthstr != "" and heightstr != "" and invalid == 0:
        width = int(widthstr)
        height = int(heightstr)
        if width < 1 or height < 1:
            print("Both dimensions must be positive.")
            dimensions = "0x0"
print("Width set to " + widthstr + "; height set to " + heightstr + ".")
area = width * height
grid = []
while grid == []:
    print("Input the grid as a continuous string of", area, "1s and 0s:")
    rawgrid = input("")
    invalid = 0
    i = 0
    for char in rawgrid:
        i += 1
        if char != "1" and char != "0" and invalid != 1:
            invalid = 1
            print("Please check the string, then input again.")
            grid = []
    if i != area:
        print("Incorrect string length; please check the grid, then input again.")
        grid = []
        invalid = 1
    if invalid == 0:
        for char in rawgrid:
            grid.append(int(char))

galaxymap = []
outgrid = ["X"]
regionsgrid = [0]               # regionsgrid initially starts as a field of zeroes,
for i in range(0, area-1):      # but then fills in according to flush regions of black/white starting at index 1;
    outgrid.append("X")         # if a cell is definitively assigned to a star, its region is set to -1
    regionsgrid.append(0)
for pointer in range(0, area):  # get initial region fills
    galaxymap.append(0)
    if regionsgrid[pointer] == 0:
        regionfill(pointer)
"""
print("Regions:")               # uncomment if you want to print initial region fills
for i in range(0, height):
    for j in range(0, width):
        outnum = regionsgrid[i*width+j]
        print("{:02d}".format(outnum), end=" ")
    print()
print()
"""
def elimgalaxy(cell):       # given a cell, we wipe the whole galaxy associated with it
    global outgrid
    global regionsgrid
    if galaxymap[cell] == 0:
        return 0
    else:
        rottengalaxy = galaxymap[cell]
        for pointer in range(0, area):
            if galaxymap[pointer] == rottengalaxy:
                outgrid[pointer] = "X"
                regionsgrid[pointer] = 0
                galaxymap[pointer] = 0

"""
to avoid puzzles which are too difficult, or which have multiple solutions, a solver is included here
once the puzzle is generated, it will be fed in, and then adjusted if insoluble
"""
unsolvedgalaxies = []
galaxytypes = ["X", "X"]
"""
the galaxytypes list:
["X", "X", the pointer value of the first dot, the first dot's type (c, r, b, d), the pointer value of the second dot...]
the first dot is numbered 1, so this makes it convenient to call dot #x's location & type with galaxytypes[2*x] & galaxytypes[2x+1]
"""
def updatesolves():
    global unsolvedgalaxies
    chkcell = 0
    galaxiestoremove = []
    for focusgalaxy in unsolvedgalaxies:
        pointer = 0
        galaxycouldbesolved = 1
        while pointer < area and galaxycouldbesolved == 1:
            if solvedgrid[pointer] == focusgalaxy:
                chkcell = pointer - 1       # check whether the galaxy could expand left at this cell
                chkflection = reflection(focusgalaxy, chkcell)
                if pointer % width != 0 and chkflection != -1:
                    if solvedgrid[chkcell] == "X":
                        galaxycouldbesolved = 0
                chkcell = pointer + 1       # check whether the galaxy could expand right at this cell
                chkflection = reflection(focusgalaxy, chkcell)
                if chkcell % width != 0 and chkflection != -1:
                    if solvedgrid[chkcell] == "X":
                        galaxycouldbesolved = 0
                chkcell = pointer - width   # check whether the galaxy could expand up at this cell
                chkflection = reflection(focusgalaxy, chkcell)
                if chkcell >= 0 and chkflection != -1:
                    if solvedgrid[chkcell] == "X":
                        galaxycouldbesolved = 0
                chkcell = pointer + width   # check whether the galaxy could expand down at this cell
                chkflection = reflection(focusgalaxy, chkcell)
                if chkcell < area and chkflection != -1:
                    if solvedgrid[chkcell] == "X":
                        galaxycouldbesolved = 0
            pointer += 1
        if galaxycouldbesolved == 1:
            # if the galaxy can't expand, it's solved, baybee
            galaxiestoremove.append(focusgalaxy)
    for galaxy in galaxiestoremove:
        unsolvedgalaxies.remove(galaxy)
        # remove all the solved galaxies so that we don't check them again
    return 0

def reflection(dotnumber, focuscell):           # returns the 180° rotation of a given cell and around its respective dot
    dotlocation = galaxytypes[2*dotnumber]
    dottype = galaxytypes[2*dotnumber+1]
    horiztweener = 0
    vertitweener = 0
    if dottype == "c":
        reflectioncell = 2 * dotlocation - focuscell           
    elif dottype == "r":
        reflectioncell = 2 * dotlocation - focuscell + 1
        horiztweener = 0.5                           # tweener accounts for half-squares when we check for horizontal offset
    elif dottype == "b":
        reflectioncell = 2 * dotlocation - focuscell + width
        vertitweener = -0.5
    elif dottype == "d":
        reflectioncell = 2 * dotlocation - focuscell + width + 1
        horiztweener = 0.5
        vertitweener = -0.5
    # now check whether our reflection answer makes sense, or if it bonked into a puzzle boundary or solved cell
    # if it bonked, then return -1 instead of a valid cell
    if reflectioncell < 0 or reflectioncell >= area:                            # for ceiling & floor
        return -1
    if reflectioncell < 0 or reflectioncell >= area:                            # for walls
        return -1
    if ((dotlocation % width) + horiztweener) != ((focuscell % width) + (reflectioncell % width))/2:
        return -1
    if ((dotlocation // width) + vertitweener) != ((focuscell // width) + (reflectioncell // width))/2:
        return -1
    if regionsgrid[dotlocation] != regionsgrid[reflectioncell]:
        return -1
    if solvedgrid[reflectioncell] != "X":                                       # for solved cells
        return -1
    return reflectioncell

solvedgrid = []

def attemptsolve():
    global outgrid
    global regionsgrid
    global galaxytypes
    global solvedgrid
    solvedgrid = []
    for i in range(0,area):
        solvedgrid.append("X")
    dotsgrid = outgrid
    numdots = 0
    # solve the obvious cells overlaid by dots while fleshing out galaxytypes and unsolvedgalaxies
    for pointer in range(0, area):
        if dotsgrid[pointer] != ".":
            numdots += 1
            unsolvedgalaxies.append(numdots)
            solvedgrid[pointer] = numdots
            galaxytypes.append(pointer)
            if str(dotsgrid[pointer]).lower() == "c":
                galaxytypes.append("c")
            elif str(dotsgrid[pointer]).lower() == "r":
                solvedgrid[pointer+1] = numdots
                galaxytypes.append("r")
            elif str(dotsgrid[pointer]).lower() == "b":
                solvedgrid[pointer+width] = numdots
                galaxytypes.append("b")
            elif str(dotsgrid[pointer]).lower() == "d":
                solvedgrid[pointer+1] = numdots
                solvedgrid[pointer+width] = numdots
                solvedgrid[pointer+width+1] = numdots
                galaxytypes.append("d")
    updatesolves()
    solvedcells = 1         # the solvedcells variable keeps track of how many cells were solved during each solver pass
    while solvedcells != 0: # if it's ever 0 by the end, we know either the puzzle is solved, or something went awry
        solvedcells = 0
        for pointer in range(0, area):
            if solvedgrid[pointer] == "X":
                validgalaxies = 0
                validgalaxylist = []
                for focusgalaxy in unsolvedgalaxies:
                    if reflection(focusgalaxy, pointer) != -1:
                        validgalaxies += 1
                        validgalaxylist.append(focusgalaxy)
                if validgalaxies == 1:                          # if we found exactly one dot which can reach the cell, solve it
                    solvedcells += 1
                    solvedreflection = reflection(validgalaxylist[0], pointer)
                    solvedgrid[pointer] = validgalaxylist[0]
                    solvedgrid[solvedreflection] = validgalaxylist[0]
    updatesolves()
    if unsolvedgalaxies == []:
        return 1
    else:   # "errm..... well this is awkward....... ur puzzle too Bad, couldn't solve.."
        print("Puzzle was generated, but no solution was found. Retrying...")
        for pointer in range(0, area):      # this is why we kept track using galaxymap
            if solvedgrid[pointer] == "X":
                elimgalaxy(pointer)
        for pointer in range(0,area):
            if regionsgrid[pointer] == 0:
                regionfill(pointer)
        return 0
"""
end solver code, begin generator code
"""

singledoubleelim()                                      # start creating puzzle by sweeping for singletons & 1x2s
puzzlefinished = 0
while puzzlefinished == 0:
    pointer = 0
    regionfound = 0
    while regionfound == 0 and pointer < area:
        if regionsgrid[pointer] > 0:
            regionfound = 1
            regiontofill = regionsgrid[pointer]
        pointer += 1                                    # find a region to focus on resolving
    if regionfound == 0:                                # if none was found, make sure the puzzle is solvable
        if "X" in outgrid:
            puzzlefinished = 0
            print("err")
        else:
            if attemptsolve() == 0: # unsolvable puzzle? place a singleton, regenerate regions, and keep generating galaxies
                pointer = 0
                while regionsgrid[pointer] < 0:         # randomly place a singleton
                    pointer += 1
                getregionalcells(regionsgrid[pointer])
                singletonpos = random.randrange(0, len(rcl))
                pointer = rcl[singletonpos]
                regionsgrid[pointer] = -1
                galaxymap[singletonpos] = galaxymapticker
                galaxymapticker += 1
                if grid[pointer] == 0:
                    outgrid[pointer] = "c"
                else:
                    outgrid[pointer] = "C"
            else:
                puzzlefinished = 1
    else:                                               # if an unresolved region was found, place a galaxy there
        getregionalcells(regiontofill)
        placegalaxy()
        singledoubleelim()

print("Finished grid:")
for i in range(0, height):
    for j in range(0, width):
        outchar = outgrid[i*width+j]
        print(outchar, end="")
    print()

jaodernein = input("Want a copy of the grid as an image? (It will be saved to the same folder as this program.) Y/N: ")
jaoderneinalnum = ""
for char in jaodernein:
    if char.isalnum:
        jaoderneinalnum = jaoderneinalnum + char
if jaoderneinalnum.lower() == "y" or jaoderneinalnum == "yes" or jaoderneinalnum == "sure" or jaoderneinalnum == "ja" or jaoderneinalnum == "ya" or jaoderneinalnum == "yeah" or jaoderneinalnum == "1" or jaoderneinalnum == "absolutely" or jaoderneinalnum == "ok" or jaoderneinalnum == "okay" or jaoderneinalnum == "alright" or jaoderneinalnum == "alrighty" or jaoderneinalnum == "allright" or jaoderneinalnum == "alrighty then" or jaoderneinalnum == "wile" or jaoderneinalnum == "indeed" or jaoderneinalnum == "ofcourse" or jaoderneinalnum == "affirmative" or jaoderneinalnum == "certainly" or jaoderneinalnum == "definitely" or jaoderneinalnum == "ye" or jaoderneinalnum == "yea" or jaoderneinalnum == "aye" or jaoderneinalnum == "ayeaye" or jaoderneinalnum == "yesh" or jaoderneinalnum == "surething" or jaoderneinalnum == "yeahman" or jaoderneinalnum == "suredude" or jaoderneinalnum == "yeahdude" or jaoderneinalnum == "sureman" or jaoderneinalnum == "yeahmate" or jaoderneinalnum == "suremate" or jaoderneinalnum == "okiedokie" or jaoderneinalnum == "mhm" or jaoderneinalnum == "uhhuh" or jaoderneinalnum == "isuredo" or jaoderneinalnum == "suredo" or jaoderneinalnum == "naturally" or jaoderneinalnum == "yep" or jaoderneinalnum == "yup" or jaoderneinalnum == "yeppers" or jaoderneinalnum == "makeitso" or jaoderneinalnum == "naturally" or jaoderneinalnum == "oui" or jaoderneinalnum == "rightyho" or jaoderneinalnum == "iguess" or jaoderneinalnum == "iguessso" or jaoderneinalnum == "yass" or jaoderneinalnum == "soundsgood" or jaoderneinalnum == "thatsoundsgood" or jaoderneinalnum == "hellyeah" or jaoderneinalnum == "hellyes" or jaoderneinalnum == "heckyeah" or jaoderneinalnum == "heckyes" or jaoderneinalnum == "verywell" or jaoderneinalnum == "verywellthen" or jaoderneinalnum == "duh" or jaoderneinalnum == "duhh" or jaoderneinalnum == "duhhh":
    genimage(width, height, outgrid)
    print("Saved!")
else:
    print("Suit yourself...")
