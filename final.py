from cmu_graphics import *

# ---- BUTTON FUNCTIONS ----
#slightly modified from cs academy
def onButton(app, mouseX, mouseY, buttonX, buttonY, width, height):
    inX = buttonX - width / 2 <= mouseX <= buttonX + width / 2
    inY = buttonY - height / 2 <= mouseY <= buttonY + height / 2
    return inX and inY

# ---- ON APP START ----
def onAppStart(app):
    #start ----------
    app.buttonWidth = 150
    app.buttonHeight = 50
    app.buttonColor = 'darkOrchid'

    #main ---------
    app.toolBoxWidth = app.width / 5
    app.graphComponents = []
    app.draggingComponent = None
    app.graphWires = [] 
    app.draggingWire = None
    app.wireStartLocation = None
    app.wireEndLocation = None
    app.dragFromInput = None #true if start point is input, false if start point is output
    app.powerOn = False 
    app.onXor = False
    app.onAdder = False

        #gates urls
    app.notGate = 'not.png'
    app.andGate = 'and.png'
    app.orGate = 'or.png'
    app.inputOn = 'inputOn.png'
    app.inputOff = 'inputOff.png'
    app.outputOn = 'outputOn.png'
    app.outputOff = 'outputOff.png'
    app.node = 'node.png'
    app.xorGate = 'xor.png'
    app.adder = 'adder.png'
    app.xorSchematic = 'xorScematic.png'
    app.adderSchematic = 'adderSchematic.png'

        #toolbox component variables
    app.gateButtonWidth = (app.toolBoxWidth-20)/2
    app.gateButtonHeight = 110
    app.leftGateButtonX = app.toolBoxWidth/4
    app.rightGateButtonX = app.toolBoxWidth*3/4
    app.notY = 120
    app.andY = 120
    app.orY = 240
    app.nodeY = 240
    app.xorY = 360
    app.adderY = 360
    app.inputY = 480
    app.outputY = 480

        #toolbox components
    app.toolboxButtons = [
        ToolboxButton(app.leftGateButtonX, app.notY, app.gateButtonWidth, app.gateButtonHeight, "NOT", NotGate,'not.png'),
        ToolboxButton(app.rightGateButtonX, app.andY, app.gateButtonWidth, app.gateButtonHeight, "AND", AndGate,'and.png'),
        ToolboxButton(app.leftGateButtonX, app.orY, app.gateButtonWidth, app.gateButtonHeight, "OR", OrGate,'or.png'),
        ToolboxButton(app.rightGateButtonX, app.nodeY, app.gateButtonWidth, app.gateButtonHeight, "NODE", Node,'node.png'),
        ToolboxButton(app.leftGateButtonX, app.xorY, app.gateButtonWidth, app.gateButtonHeight, "XOR", XorGate,'xor.png'),
        ToolboxButton(app.rightGateButtonX, app.adderY, app.gateButtonWidth, app.gateButtonHeight, "ADDER", Adder,'adder.png'),
        ToolboxButton(app.leftGateButtonX, app.inputY, app.gateButtonWidth, app.gateButtonHeight, "INPUT", Input,'inputOn.png'),
        ToolboxButton(app.rightGateButtonX, app.outputY, app.gateButtonWidth, app.gateButtonHeight, "OUTPUT", Output,'outputOn.png')
    ]
    app.powerButton = PowerButton(app.toolBoxWidth/2, 600, app.toolBoxWidth-20, 50)
    app.expressionButton = ExpressionButton(app.toolBoxWidth/2, 660, app.toolBoxWidth-20, 50)
    app.resetButton = ResetButton(app.toolBoxWidth/2, 720,app.toolBoxWidth-20,50)
    
    #expr ----------
    app.backButton = BackButton(100,75,100,50, 'yellow', 'coral')
    app.expressionText = generateExpression(app)
    app.expressions = {}
    app.visited = set()

    #xor ---------
    app.xorBackButton = BackButton(100,75,100,50, 'white', 'black')

    #adder --------
    app.adderBackButton = BackButton(100,75,100,50, 'white', 'black')

    #output --------
    app.outputErrorBackButton = BackButton(100,75,100,50, 'hotPink', 'deepPink')
    
# ---- START SCREEN ----
#draws the start screen with instructions and a start button
def drawStartScreen(app):
    #fill background
    drawRect(0, 0, app.width, app.height, fill='plum')
    #title/instructions
    drawLabel("GATE GURU", app.width / 2, app.height / 4, fill='white',
              font='Orbitron font', size=150, bold=True, border='darkOrchid')
    drawLabel('Instructions: Click the start button! Drag and drop components from the toolbox into the workspace.',
              app.width / 2, app.height / 2 - 30, fill="darkOrchid", size=24, font='Times')
    drawLabel('Hit the power button to visualize the circuit.',
              app.width / 2, app.height / 2 + 30, fill="darkOrchid", size=24, font='Times')
    #start button          
    drawRect(app.width / 2, app.height * 0.75, app.buttonWidth, app.buttonHeight,
             fill=app.buttonColor, align="center", borderWidth=5, border='white')
    drawLabel('START', app.width / 2, app.height * 0.75, fill='white', font='Orbitron font', size=30)

#cmu graphics
def start_onMouseMove(app, mouseX, mouseY):
    #if mouse on button, changes color
    if onButton(app, mouseX, mouseY, app.width / 2, app.height * 0.75, app.buttonWidth, app.buttonHeight):
        app.buttonColor = 'orchid'
    else:
        app.buttonColor = 'darkOrchid'

def start_onMousePress(app, mouseX, mouseY):
    #if start button pressed, go to main screen
    if onButton(app, mouseX, mouseY, app.width / 2, app.height * 0.75, app.buttonWidth, app.buttonHeight):
        setActiveScreen('main')

def start_redrawAll(app):
    drawStartScreen(app)




# ---- MAIN SCREEN ----
# this function draws the background for the main screen
# there will be graph paper on the right and a column on the left for the toolbox components.
# there will also be a note at the bottom about how hovering over complex gates will display the schematic
def drawBackground(app):
    #drawing graph paper background
    drawRect(app.toolBoxWidth, 0, app.width, app.height, fill='cornSilk')
    for i in range(int(app.toolBoxWidth)+25, int(app.width)-25,25):
        for j in range (25, app.height-25, 25):
            drawCircle(i,j,1)
    #drawing toolbox
    drawRect(0, 0, app.toolBoxWidth, app.height, fill='paleTurquoise')
    drawLabel("TOOLBOX", app.toolBoxWidth / 2, 25, font="Times", size=36)
    drawLabel("To see schematic for complex gates, hover over component and press the space bar", 
              (app.width-app.toolBoxWidth)/2+app.toolBoxWidth, 750, size = 18, font = "Times")
    
def main_onMouseMove(app,mouseX,mouseY):
    #checks to see if mouse is on "complex gates"
    for component in app.graphComponents:
        if isinstance(component, XorGate):
            if component.hover(mouseX,mouseY):
                app.onXor = True
            else:
                app.onXor = False
        elif isinstance(component, Adder):
            if component.hover(mouseX,mouseY):
                app.onAdder = True
            else:
                app.onAdder = False

def main_onKeyPress(app,key):
    if key == 'space':
        if app.onXor:
            setActiveScreen('xor') #switch to XOR schematic
        elif app.onAdder:
            setActiveScreen('adder') #switch to Adder Schematic

def main_onMousePress(app, mouseX, mouseY):
    #dragging from toolbox onto the schematic
    for component in app.toolboxButtons:
        if component.isClicked(mouseX, mouseY):
            compType = component.componentClass
            if compType == NotGate:
                imageWidth, imageHeight = getImageSize(app.notGate)
                app.draggingComponent = NotGate(component.x, component.y, imageWidth, imageHeight)
            elif compType == AndGate:
                imageWidth, imageHeight = getImageSize(app.andGate)
                app.draggingComponent = AndGate(component.x, component.y, imageWidth, imageHeight)
            elif compType == OrGate:
                imageWidth, imageHeight = getImageSize(app.orGate)
                app.draggingComponent = OrGate(component.x, component.y, imageWidth, imageHeight)
            elif compType == XorGate:
                imageWidth, imageHeight = getImageSize(app.xorGate)
                app.draggingComponent = XorGate(component.x, component.y, imageWidth, imageHeight)
            elif compType == Adder:
                imageWidth, imageHeight = getImageSize(app.adder)
                # change dimensions to fit more cohesively with sizes of other gates
                app.draggingComponent = Adder(component.x, component.y, 0.8*imageWidth, 0.8*imageHeight)
            elif compType == Input:
                imageWidth, imageHeight = getImageSize(app.inputOn)
                app.draggingComponent = Input(component.x, component.y, imageWidth, imageHeight, False)
            elif compType == Output:
                if len(Output.gates)<1: #only one output!
                    imageWidth, imageHeight = getImageSize(app.outputOff)
                    app.draggingComponent = Output(component.x, component.y, imageWidth, imageHeight, False)
                else:
                    setActiveScreen('outputError') # changes screen to multiple output error screen
                    break
            elif compType == Node:
                imageWidth, imageHeight = getImageSize(app.node)
                app.draggingComponent = Node(component.x, component.y, imageWidth, imageHeight)
            
            app.draggingComponent.x, app.draggingComponent.y = mouseX, mouseY
            break

    #objects in schematic
    for component in app.graphComponents:
        if component.isClicked(mouseX, mouseY):
            # Toggle Input if clicked !
            if isinstance(component, Input):
                component.toggle()
        
        # New wire initiation
        startInputIndex = component.getInputPointIndex(mouseX, mouseY)
        startOutputIndex = component.getOutputPointIndex(mouseX, mouseY)
        if startOutputIndex is not None and mouseX > app.toolBoxWidth:
            # Start dragging from an output point
            app.draggingWire = True
            app.dragFromInput = False  # Dragging from output
            app.wireStartComponent = component
            app.wireStartPointType = 'output'
            app.wireStartPointIndex = startOutputIndex
            app.wireStartLocation = component.outputPoints[startOutputIndex]
            break  # Assume only one wire can be dragged at a time
        elif startInputIndex is not None and mouseX > app.toolBoxWidth:
            # Start dragging from an input point
            app.draggingWire = True
            app.dragFromInput = True  # Dragging from input
            app.wireStartComponent = component
            app.wireStartPointType = 'input'
            app.wireStartPointIndex = startInputIndex
            app.wireStartLocation = component.inputPoints[startInputIndex]
            break

    # Power button clicked
    if app.powerButton.isClicked(mouseX, mouseY):
        powerCircuit(app)

    # Expression button
    if app.expressionButton.isClicked(mouseX,mouseY):
        app.expressionText = generateExpression(app)
        setActiveScreen('expression')

    # Reset button
    if app.resetButton.isClicked(mouseX,mouseY):
        reset(app)


def powerCircuit(app):
    # this function should go through and update the wire color and status 
    # if the power is on, the wire color is updated based on what output value is being passed through it
    # if the power is off thw wires shoud all turn black and be set to False.
    app.powerOn = not app.powerOn

    if app.powerOn:
        # Update all component values and wire states
        for component in app.graphComponents:
            if isinstance(component, Component):
                component.updateValue()
        for wire in app.graphWires:
            wire.updateState()
    else:
        # Reset all components to default
        for component in app.graphComponents:
            component.outputValue = False
            component.inputValue = False
            if isinstance(component, Adder):
                component.sum = False
                component.carry = False
            elif isinstance(component, AndGate) or isinstance(component, OrGate) or isinstance(component, XorGate):
                component.inputA = False
                component.inputB = False
            elif isinstance(component, Input):
                component.outputValue = component.on  # Input retains its toggle state

        for wire in app.graphWires:
            wire.color = 'black'


def reset(app):
    #this function resets the whole screen and rests every setting back to the default setting.
    app.graphComponents = []
    app.draggingComponent = None
    app.graphWires = [] 
    app.draggingWire = None
    app.wireStartLocation = None
    app.wireEndLocation = None
    app.dragFromInput = None #true if start point is input, false if start point is output
    app.powerOn = False 
    Input.labelCounter = 0
    AndGate.gates = []
    OrGate.gates = []
    NotGate.gates = []
    Node.gates = []
    XorGate.gates = []
    Adder.gates = []
    Input.gates = []
    Output.gates = []



def main_onMouseDrag(app, mouseX, mouseY):
    if app.draggingComponent:
        app.draggingComponent.x, app.draggingComponent.y = mouseX, mouseY
        app.draggingComponent.updatePoints()

    # Show wire path while dragging
    if app.draggingWire:
        app.wireEndLocation = (mouseX, mouseY)

def main_onMouseRelease(app, mouseX, mouseY):
    # Add to schematic if dragged past toolbox
    if app.draggingComponent:
        if mouseX > app.toolBoxWidth:
            app.graphComponents.append(app.draggingComponent)
            compType = app.draggingComponent.getCompType()
            compType.gates.append(app.draggingComponent)
        elif isinstance(app.draggingComponent, Output): #reset count if not in schematic
            Output.gates = []
        app.draggingComponent = None

    # Establish wire if valid
    if app.draggingWire:
        endComponent = None
        endPointType = None
        endPointIndex = None

        # Find the end component and connection index based on where the wire is dragged to
        for component in app.graphComponents:
            if app.dragFromInput:
                # Dragging from input 
                possibleTypes = ['output', 'input']  # Allow connecting to both
                for pointType in possibleTypes:
                    if pointType == 'output':
                        index = component.getOutputPointIndex(mouseX, mouseY)
                    else:
                        index = component.getInputPointIndex(mouseX, mouseY)

                    if index is not None:
                        endComponent = component
                        endPointType = pointType
                        endPointIndex = index
                        break
                if endComponent:
                    break
            else:
                # Dragging from output
                possibleTypes = ['input', 'output']
                for pointType in possibleTypes:
                    if pointType == 'input':
                        index = component.getInputPointIndex(mouseX, mouseY)
                    else:
                        index = component.getOutputPointIndex(mouseX, mouseY)

                    if index is not None:
                        endComponent = component
                        endPointType = pointType
                        endPointIndex = index
                        break
                if endComponent:
                    break

        # Validate the connection
        if endComponent:
            # Prevent connecting to self
            if endComponent == app.wireStartComponent and endPointType == app.wireStartPointType and endPointIndex == app.wireStartPointIndex:
                pass # cannot connect to itself
            else:
                # Prevent duplicate connections
                duplicate = False
                for wire in app.graphWires:
                    if (wire.startComponent == app.wireStartComponent and
                        wire.startPointType == app.wireStartPointType and
                        wire.startPointIndex == app.wireStartPointIndex and
                        wire.endComponent == endComponent and
                        wire.endPointType == endPointType and
                        wire.endPointIndex == endPointIndex):
                        duplicate = True
                        break

                if not duplicate:
                    validConnection = False  # Initialize variable with a default value

                    # Prevent multiple wires to the same input point
                    if endPointType == 'input':
                        for wire in app.graphWires:
                            if wire.endComponent == endComponent and wire.endPointType == 'input' and wire.endPointIndex == endPointIndex:
                                break # already has wire connected
                        else:
                            validConnection = True
                    else:
                        validConnection = True

                    if validConnection:
                        # Create and add the wire
                        newWire = Wire(
                            app.wireStartComponent,
                            app.wireStartPointType,
                            app.wireStartPointIndex,
                            endComponent,
                            endPointType,
                            endPointIndex
                        )
                        app.graphWires.append(newWire)
                        # Update component connections based on point types
                        if app.dragFromInput:
                            if endPointType == 'output':
                                app.wireStartComponent.connections['inputs'].append(endComponent)
                                endComponent.connections['outputs'].append(app.wireStartComponent)
                        else:
                            if endPointType == 'input':
                                app.wireStartComponent.connections['outputs'].append(endComponent)
                                endComponent.connections['inputs'].append(app.wireStartComponent)



    # Reset dragging state
    app.draggingWire = False
    app.wireStartComponent = None
    app.wireStartPointType = None
    app.wireStartPointIndex = None
    app.wireEndLocation = None


 
def validWire(app, mouseX, mouseY, startComponent):
    #this function generates a valid Wire based on the current mouse position and the starting component
    #if the function starts from an input point it is only allowed to connect to an output point of another component
    for component in app.graphComponents:
        if (component != startComponent and #not same object
            ((component.onInput(mouseX,mouseY) and not app.dragFromInput) #output to input
             or (component.onOutput(mouseX,mouseY) and app.dragFromInput))): #input to output
            return component
    return None

def hasCycle(startComponent, endComponent, visited=None):
    # returns boolean value
    # whether adding connection from start to end component makes a loop
    # true if cycle created

    if visited is None:
        visited = set()
    if startComponent == endComponent:
        return True
    visited.add(startComponent)
    for output_component in startComponent.connections['outputs']:
        if output_component not in visited:
            if hasCycle(output_component, endComponent, visited):
                return True
    return False

    

def main_redrawAll(app):
    drawBackground(app)

    # Draw toolbox buttons
    for button in app.toolboxButtons:
        button.draw()

    # Draw control buttons
    app.powerButton.draw(app)
    app.expressionButton.draw()
    app.resetButton.draw()

    # Draw existing wires
    for wire in app.graphWires:
        wire.updateState()
        wire.draw()

    # Draw existing components
    for component in app.graphComponents:
        component.draw()

    # Draw dragging component
    if app.draggingComponent:
        app.draggingComponent.draw()

    # Draw wire being dragged
    if app.draggingWire and app.wireStartLocation and app.wireEndLocation:
        x0, y0 = app.wireStartLocation
        x1, y1 = app.wireEndLocation
        drawLine(x0, y0, x1, y1, fill='gray', lineWidth=2, dashes=True)
        

# ---- TOOLBOX BUTTONS ----
class ToolboxButton:
    def __init__(self, x, y, width, height, text, componentClass,url = None):
        self.x = x
        self.y = y
        self.text = text
        self.componentClass = componentClass
        self.url = url
        self.width = width
        self.height = height

    def draw(self):
        # this function draws the button 
        # special case for the adder button so that the proportions for the gate drawing shrink.
        drawRect(self.x, self.y, self.width, self.height, fill='lightSkyBlue',
                 border='deepSkyBlue', borderWidth=5, align = 'center')
        drawLabel(self.text, self.x, self.y + 40, size=15, bold=True, font='Times')
        if self.componentClass == Adder:
            drawLabel(self.text, self.x, self.y , size=24, bold=True, font='Times')

        else:
            drawImage(self.url, self.x, self.y, align = 'center')
            drawLabel(self.text, self.x, self.y + 40, size=15, bold=True, font='Times')
        

    def isClicked(self, mouseX, mouseY):
        # This function returns a boolean function based on whether the button is clicked on not
        # called on mouse press
        # returns whether mouse is on the button
        return self.x - self.width / 2 <= mouseX <= self.x + self.width / 2 and \
               self.y - self.height / 2 <= mouseY <= self.y + self.height / 2
    

class PowerButton:
    def __init__(self,x,y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = 'crimson'
        self.label = 'POWER'

    def draw(self,app):
        # this function draws the button
        # red if power if off with text "POWER"
        # green if power is on with text "SHUT DOWN"
        if app.powerOn:
            self.label = 'SHUT DOWN'
            self.color = 'yellowGreen'
        else:
            self.label = "POWER"
            self.color = 'crimson'
        drawRect(self.x, self.y, self.width, self.height, fill = self.color,
                 border = 'white', borderWidth = 5, align = 'center')
        drawLabel(self.label, self.x, self.y, size = 24, bold = True, font = 'Times', fill = 'white')

    def isClicked(self, mouseX, mouseY):
        # This function returns a boolean function based on whether the button is clicked on not
        # called on mouse press
        # returns whether mouse is on the button
        return self.x - self.width / 2 <= mouseX <= self.x + self.width / 2 and \
               self.y - self.height / 2 <= mouseY <= self.y + self.height / 2
    
class ExpressionButton:
    def __init__(self,x,y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        # draws a button that reroutes to the expression screen
        drawRect(self.x, self.y, self.width, self.height, fill = 'hotPink',
                 border = 'white', borderWidth = 5, align = 'center')
        drawLabel("EXPRESSION", self.x, self.y, size = 24, bold = True, font = 'Times', fill = 'white')


    def isClicked(self, mouseX, mouseY):
        # This function returns a boolean function based on whether the button is clicked on not
        # called on mouse press
        # returns whether mouse is on the button
        return self.x - self.width / 2 <= mouseX <= self.x + self.width / 2 and \
               self.y - self.height / 2 <= mouseY <= self.y + self.height / 2
    
class ResetButton:
    def __init__(self,x,y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        # draws a button that calls a function to a reset function
        drawRect(self.x, self.y, self.width, self.height, fill = 'darkOrange',
                 border = 'white', borderWidth = 5, align = 'center')
        drawLabel("RESET", self.x, self.y, size = 24, bold = True, font = 'Times', fill = 'white')

    def isClicked(self, mouseX, mouseY):
        # This function returns a boolean function based on whether the button is clicked on not
        # called on mouse press
        # returns whether mouse is on the button
        return self.x - self.width / 2 <= mouseX <= self.x + self.width / 2 and \
               self.y - self.height / 2 <= mouseY <= self.y + self.height / 2
                

# ---- GATE CLASSES ----
class Component:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width-20
        self.height = height-20
        self.connections = {"inputs": [], "outputs": []}
        self.inputCapacity = None
        self.inputPoints = []
        self.outputPoints = []

    def getInputPointIndex(self, mouseX, mouseY):
        # returns the index of the input point if mouse is over it
        # returns None otherwise
        index = 0
        for inputPoint in self.inputPoints:
            inputX, inputY = inputPoint
            if (abs(mouseX - inputX) <= 5) and (abs(mouseY - inputY) <= 5):
                return index
            index += 1
        return None

    def getOutputPointIndex(self, mouseX, mouseY):
        # returns the index of the output point if mouse is over it
        # returns None otherwise
        index = 0
        for outputPoint in self.outputPoints:
            outputX, outputY = outputPoint
            if (abs(mouseX - outputX) <= 5) and (abs(mouseY - outputY) <= 5):
                return index
            index += 1
        return None


    def addConnection(self, connectingComponent, connectionType):
        # this adds a connection to the self compoennt object
        # only adds connection if there is a capacity for it to be added as an input
        # unlimited output connections
        if (connectionType == 'inputs' and self.inputCapacity > len(self.connections['inputs']))or connectionType =='outputs': #only limited
            self.connections[connectionType].append(connectingComponent)

    def isInputPoint(self, point):
        # this function returns a boolean value
        # returns True if mouse on input.
        for inputPoint in self.inputPoints:
            if inputPoint == point:
                return True
        return False
    
    def isOutputPoint(self, point):
        # this function returns a boolean value
        # returns True if mouse is on output.
        for output_point in self.outputPoints:
            if output_point == point:
                return True
        return False

    
    def drawCircles(self):
        #this function draws circles to mark the input and output points
        # cyan circles for inputs
        # red crcles for outputs

        # Draw input points
        for (inputX, inputY) in self.inputPoints:
            drawCircle(inputX, inputY, 5, fill='cyan', border="black")
        # Draw output points
        for (outputX, outputY) in self.outputPoints:
            drawCircle(outputX, outputY, 5, fill='red', border="black")


    def isClicked(self, mouseX, mouseY):
        # This function returns a boolean function based on whether the button is clicked on not
        # called on mouse press
        # returns whether mouse is on the button
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        top = self.y - self.height / 2
        bottom = self.y + self.height / 2

        return left <= mouseX <= right and top <= mouseY <= bottom
    
    def getCompType(self):
        # this function returns the component type of the object this function is called upon
        if isinstance(self, NotGate):
            return NotGate
        if isinstance(self, AndGate):
            return AndGate
        if isinstance(self, OrGate):
            return OrGate
        if isinstance(self, XorGate):
            return XorGate
        if isinstance(self, Adder):
            return Adder
        if isinstance(self, Node):
            return Node
        if isinstance(self, Input):
            return Input
        if isinstance(self, Output):
            return Output
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return isinstance(other, Component) and self.getCompType() == other.getCompType() and self.index == other.index


class NotGate(Component):
    gates = []
    def __init__(self, x, y, width, height):
        self.type = 'NOT'
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = len(NotGate.gates)
        self.connections = {"inputs": [], 'outputs': []}
        NotGate.gates.append(self)
        self.inputMargin = 20
        self.outputMargin = 15
        self.updatePoints()
        self.inputValue = None
        self.outputValue = None
        self.inputCapacity = 1


    def updateValue(self):
        # This function updates the output value based on the input value
        if self.connections["inputs"]:
            inputComponent = self.connections["inputs"][0]
            self.inputValue = inputComponent.outputValue 
            self.outputValue = not self.inputValue 
        else:
            self.inputValue = False
            self.outputValue = True

    def updatePoints(self):
        # this function moves the output and input markers to move with the dragged component
        self.inputPoints = [(self.x - self.width // 2 + self.inputMargin, self.y)]  # Left side input
        self.outputPoints = [(self.x + self.width // 2 - self.outputMargin, self.y)]

    def onInput(self, mouseX, mouseY):
        # this function returns a boolean value
        # returns whether or not the  mouse is on a input marker
        return (5 < abs(self.x-self.width//2-mouseX)) and (5 < abs(self.y-mouseY))
    

    def onOutput(self,mouseX,mouseY):
        #this function returns a boolean value
        # returns whether or not the mouse is on a input marker
        return (5 < abs(self.x-self.width//2-mouseX)) and (5 < abs(self.y-mouseY))

    def draw(self, app = app):
        # draws component
        # imports image and updates input and output markers
        drawImage(app.notGate, self.x, self.y, align = 'center')
        self.drawCircles()


class AndGate(Component):
    gates = []
    def __init__(self, x, y, width, height):
        self.type = 'AND'
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = len(AndGate.gates)
        self.connections = {"inputs": [], 'outputs': []}
        AndGate.gates.append(self)
        self.inputMargin = 25
        self.outputMargin = 15
        self.updatePoints()
        self.inputA = False
        self.inputB = False
        self.outputValue = False
        self.inputCapacity = 2

    def updateValue(self):
        # updates the output value based on what value is being passed thorugh the input
        if len(self.connections["inputs"]) == 2:
            inputAComponent = self.connections["inputs"][0]
            inputBComponent = self.connections["inputs"][1]
            self.inputA = inputAComponent.outputValue
            self.inputB = inputBComponent.outputValue
            self.outputValue = self.inputA and self.inputB
        else:
            self.inputA = self.inputB = False
            self.outputValue = False

    def updatePoints(self):
        # updates the input and output markers based on where component is dragged
        self.inputPoints = [(self.x - self.width // 2 + self.inputMargin, self.y - self.height // 4), #input A
                            (self.x - self.width // 2 + self.inputMargin, self.y + self.height // 4)]  # inputB
        self.outputPoints = [(self.x + self.width // 2 - self.outputMargin, self.y)]  # output

    def onInput(self, mouseX, mouseY):
        # returns a boolean value
        # return value whether or not mouse is on an input point
        return (5 < abs(self.x-self.width//2-mouseX)) and (5 < abs(self.y-self.height//4-mouseY))
    
    def onOutput(self,mouseX,mouseY):
        # returns a boolean value
        # return value whether or not maouse is on an output point
        return (5 < abs(self.x-self.width//2-mouseX)) and (5 < abs(self.y-mouseY))

    def draw(self, app = app):
        # draws component
        # imports image and updates input and output markers
        drawImage(app.andGate, self.x, self.y, align = 'center')
        self.drawCircles()


class OrGate(Component):
    gates = []
    def __init__(self, x, y, width, height):
        self.type = 'OR'
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = len(OrGate.gates)
        self.connections = {"inputs": [], 'outputs': []}
        OrGate.gates.append(self)
        self.inputMargin = 25
        self.outputMargin = 20
        self.updatePoints()
        self.inputA = False
        self.inputB = False
        self.outputValue = False
        self.inputCapacity = 2

    def updateValue(self):
        # updates the output value based on what value is being passed through the input
        if len(self.connections["inputs"]) == 2:
            inputAComponent = self.connections["inputs"][0]
            inputBComponent = self.connections["inputs"][1]
            self.inputA = inputAComponent.outputValue
            self.inputB = inputBComponent.outputValue
            self.outputValue = self.inputA or self.inputB
        else:
            self.inputA = self.inputB = False
            self.outputValue = False

    def updatePoints(self):
        # updates the input and output markers based on where component is dragged
        self.inputPoints = [(self.x - self.width // 2 + self.inputMargin, self.y - self.height // 4), #input A
                            (self.x - self.width // 2 + self.inputMargin, self.y + self.height // 4)]  # inputB
        self.outputPoints = [(self.x + self.width // 2 - self.outputMargin, self.y)]  # output


    def onInput(self,mouseX,mouseY):
        # returns a boolean value
        # return value whether or not mouse is on an input point
        return (5 < abs(self.x-self.width//2-mouseX)) and (5 < abs(self.y-self.height//4-mouseY))
    

    def onOutput(self,mouseX,mouseY):
        # returns a boolean value
        # return value whether or not mouse is on an output point
        return (5 < abs(self.x-self.width//2-mouseX)) and (5 < abs(self.y-mouseY))

    def draw(self, app = app):
        # draws component
        # imports image and updates input and output markers
        drawImage(app.orGate, self.x, self.y, align = 'center')
        self.drawCircles()

class XorGate(Component):
    gates = []
    def __init__(self, x, y, width, height):
        self.type = 'XOR'
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = len(XorGate.gates)
        self.connections = {"inputs": [], 'outputs': []}
        XorGate.gates.append(self)
        self.inputMargin = 15
        self.outputMargin = 15
        self.updatePoints()
        self.inputA = False
        self.inputB = False
        self.outputValue = False
        self.inputCapacity = 2

    def updateValue(self):
        # updates the output value based on what value is being passed thorugh the input
        if len(self.connections["inputs"]) == 2:
            inputAComponent = self.connections["inputs"][0]
            inputBComponent = self.connections["inputs"][1]
            self.inputA = inputAComponent.outputValue
            self.inputB = inputBComponent.outputValue
            self.outputValue = (self.inputA and not self.inputB) or (self.inputB and not self.inputA)
        else:
            self.inputA = self.inputB = False
            self.outputValue = False

    def updatePoints(self):
        # updates the input and output markers based on where component is dragged
        self.inputPoints = [(self.x - self.width // 2 + self.inputMargin, self.y - self.height // 4), #input A
                            (self.x - self.width // 2 + self.inputMargin, self.y + self.height // 4)]  # inputB
        self.outputPoints = [(self.x + self.width // 2 - self.outputMargin, self.y)]  # output

    def onInput(self,mouseX,mouseY):
        # returns a boolean value
        # return value whether or not mouse is on an input point
        return (5 < abs(self.x-self.width//2-mouseX)) and (5 < abs(self.y-self.height//4-mouseY))
    

    def onOutput(self,mouseX,mouseY):
        # returns a boolean value
        # return value whether or not mouse is on an output point
        return (5 < abs(self.x-self.width//2-mouseX)) and (5 < abs(self.y-mouseY))

    def draw(self, app = app):
        # draws component
        # imports image and updates input and output markers
        drawImage(app.xorGate, self.x, self.y, align = 'center')
        self.drawCircles()

    def hover(self, mouseX, mouseY):
        # returns a boolean value
        # whether or not mouse is on component
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        top = self.y - self.height / 2
        bottom = self.y + self.height / 2

        return left <= mouseX <= right and top <= mouseY <= bottom

class Adder(Component):
    gates = []
    def __init__(self, x, y, width, height):
        self.type = 'ADDER'
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = len(Adder.gates)
        self.connections = {"inputs": [], 'outputs': []}
        Adder.gates.append(self)
        self.inputMargin = 5
        self.outputMargin = 5
        self.updatePoints()
        self.inputA = False
        self.inputB = False
        self.sum = False
        self.carry = False
        self.inputCapacity = 2
        self.outputValue = None

    def updateValue(self):
        # updates the output value based on what value is being passed thorugh the input
        if len(self.connections["inputs"]) == 2:
            inputAComponent = self.connections["inputs"][0]
            inputBComponent = self.connections["inputs"][1]
            self.inputA = inputAComponent.outputValue
            self.inputB = inputBComponent.outputValue
            self.sum = self.inputA != self.inputB  # XOR
            self.carry = self.inputA and self.inputB  # AND
        else:
            self.inputA = self.inputB = False
            self.sum = self.carry = False
        

    def updatePoints(self):
     # updates the input and output markers based on where component is dragged
        self.inputPoints = [(self.x - self.width // 2 + self.inputMargin, self.y - self.height // 4), #input A
                            (self.x - self.width // 2 + self.inputMargin, self.y + self.height // 4)]  # inputB
        self.outputPoints = [(self.x + self.width // 2 - self.outputMargin, self.y - self.height // 4), # sum
                             (self.x + self.width // 2 - self.outputMargin, self.y + self.height // 4)]  # carry

    def onInput(self,mouseX,mouseY):
        # returns a boolean value
        # return value whether or not mouse is on an input point
        return (5 < abs(self.x-self.width//2-mouseX)) and (5 < abs(self.y-self.height//4-mouseY))
    
    def onOutput(self,mouseX,mouseY):
        # returns a boolean value
        # return value whether or not mouse is on an output point
        return (5 < abs(self.x-self.width//2-mouseX)) and (5 < abs(self.y-mouseY))

    def draw(self, app = app):
        # draws component
        # imports image and updates input and output markers
        imageWidth, imageHeight = getImageSize(app.adder)
        drawImage(app.adder, self.x, self.y, align = 'center',
                  width = 0.8* imageWidth, height = 0.8* imageHeight)
        self.drawCircles()

    def hover(self, mouseX, mouseY):
        # returns a boolean value
        # whether or not mouse is on component
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        top = self.y - self.height / 2
        bottom = self.y + self.height / 2

        return left <= mouseX <= right and top <= mouseY <= bottom


class Input(Component):
    gates = []
    labelCounter = 0
    def __init__(self, x, y, width, height, on=False):
        self.type = 'INPUT'
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on = on
        self.connections = {"inputs": [], 'outputs': []}
        self.inputPoints = []
        self.outputPoints = [(x, y)]
        self.index = len(Input.gates)
        self.outputValue = self.on
        self.inputCapacity = 0
        Input.gates.append(self)
        self.label = chr(ord('A')+Input.labelCounter)
        Input.labelCounter += 1

    def updatePoints(self):
        # Recalculates the position of the output points based on the current (x, y).
        self.inputPoints = []
        self.outputPoints = [(self.x + self.width // 2 - 10, self.y)]

    def updateValue(self):
        # updates the output value based on what value is being passed thorugh the input
        self.outputValue = self.on

    def onInput(self,mouseX,mouseY):
        # returns a boolean value
        # always false because input has no input pin
        return False
    
    def onOutput(self,mouseX,mouseY):
        # returns a boolean value
        # return value whether or not mouse is on an output point
        return (abs(mouseX-(self.x + self.width // 2 - 10)) < 5 and abs(mouseY - self.y)<5)

    def draw(self, app = app):
        # draws component
        # imports image based on the state of the component
        if self.on:
            drawImage(app.inputOn, self.x, self.y, align = 'center')
        else:
            drawImage(app.inputOff, self.x, self.y, align = 'center')
        drawLabel(self.label, self.x, self.y+25, size = 24)
        self.drawCircles()

    def toggle(self):
        # toggles state to opposite state
        self.on = not self.on
        self.updateValue()

    def getLabel(self):
        # returns the label that refers for the object
        return self.label



class Output(Component):
    gates = []
    def __init__(self, x, y, width, height, on=False):
        self.type = 'OUTPUT'
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on = on
        self.inputPoints = [(x, y)]
        self.outputPoints = []
        self.index = len(Output.gates)
        Output.gates.append(self)
        self.connections = {"inputs": [], 'outputs': []}
        self.inputValue = None
        self.outputValue = None
        self.inputCapacity = 1

    def updatePoints(self):
        # Recalculates the position of the input points based on the current (x, y).
        self.inputPoints = [(self.x - self.width // 2 + 10, self.y)]
        self.outputPoints = []

    def updateValue(self):
        # updates the output value based on what value is being passed thorugh the input
        if self.connections["inputs"]:
            inputComponent = self.connections["inputs"][0]
            self.inputValue = inputComponent.outputValue
            self.outputValue = self.inputValue
            self.on = self.inputValue
        else:
            self.inputValue = False
            self.outputValue = False
            self.on = False

    def onOutput(self,mouseX,mouseY):
        # returns a boolean value
        # always False because Output has no output pin
        return False
    
    def onInput(self,mouseX,mouseY):
        # returns a boolean value
        # return value whether or not mouse is on an input point
        return (abs(mouseX - (self.x - self.width // 2 + 10)) <= 5) and (abs(mouseY - self.Y) <= 5)


    def draw(self, app = app):
        # draws component
        # imports image based on the state of the component
        if self.on:
            drawImage(app.outputOn, self.x, self.y, align = 'center')
        else:
            drawImage(app.outputOff, self.x, self.y, align = 'center')
        self.drawCircles()

    def toggle(self):
        # toggles state to opposite state
        self.on = not self.on
        self.outputValue = self.on
        self.updateValue()



class Node(Component):
    gates = []
    def __init__(self, x, y, width, height):
        self.type = 'NODE'
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inputPoints = [(x, y)] 
        self.outputPoints = [(x, y)]
        self.index = len(Node.gates)
        Node.gates.append(self)
        self.connections = {"inputs": [], 'outputs': []}
        self.inputCapacity = 1
        self.inputValue = self.outputValue = None
        self.updatePoints()

    def updatePoints(self):
        # this function moves the output and input markers to move with the dragged component
        self.inputPoints = [(self.x - self.width // 2 + 10, self.y)]
        self.outputPoints = [(self.x + self.width // 2 - 10, self.y)]

    def onOutput(self,mouseX,mouseY):
        # returns a boolean value
        # return value whether or not mouse is on an output point
        return (abs(mouseX - (self.x - self.width // 2 - 10)) <= 5) and (abs(mouseY - self.Y) <= 5)
    
    def onInput(self,mouseX,mouseY):
        # returns a boolean value
        # return value whether or not mouse is on an input point
        return (abs(mouseX - (self.x - self.width // 2 + 10)) <= 5) and (abs(mouseY - self.Y) <= 5)


    def updateValue(self):
        # updates output value based on the input value being passed through
        if self.connections["inputs"]:
            inputComponent = self.connections["inputs"][0]
            self.inputValue = inputComponent.outputValue
            self.outputValue = self.inputValue
        else:
            self.inputValue = False
            self.outputValue = False

    def draw(self, app = app):
        # imports and draws image of node
        drawImage(app.node, self.x, self.y, align = 'center')
        self.drawCircles()

class Wire:
    def __init__(self, startComponent, startPointType, startPointIndex, endComponent, endPointType, endPointIndex):
        self.startComponent = startComponent
        self.startPointType = startPointType  # 'input' or 'output'
        self.startPointIndex = startPointIndex
        self.endComponent = endComponent
        self.endPointType = endPointType      # 'input' or 'output'
        self.endPointIndex = endPointIndex
        self.color = 'black'

    def updateState(self, app = app):
        # Updates the color of the wire based on the state of the start component.
        if not app.powerOn:
            # If power is off, wires remain black
            self.color = 'black'
            return
        
        if self.startPointType == 'output':
            if isinstance(self.startComponent, (Node, NotGate, AndGate, OrGate, XorGate)):
                state = self.startComponent.outputValue
            elif isinstance(self.startComponent, Adder):
                if self.startPointIndex == 0:  # Sum output
                    state = self.startComponent.sum
                elif self.startPointIndex == 1:  # Carry output
                    state = self.startComponent.carry
            elif isinstance(self.startComponent, Input):
                state = self.startComponent.outputValue
        elif self.startPointType == 'input':
            if isinstance(self.startComponent, Node):
                state = self.startComponent.inputValue
            elif isinstance(self.startComponent, (AndGate, OrGate, XorGate, Adder)):
                if self.startPointIndex == 0:  # Input A
                    state = self.startComponent.inputA
                elif self.startPointIndex == 1:  # Input B
                    state = self.startComponent.inputB
            elif isinstance(self.startComponent, Output):
                state = self.startComponent.inputValue

        self.color = 'red' if state else 'black'

    def draw(self):
        # Draws the wire dynamically based on the current positions of the connection points.
        if self.startPointType == 'output':
            startPoint = self.startComponent.outputPoints[self.startPointIndex]
        else:  # input
            startPoint = self.startComponent.inputPoints[self.startPointIndex]

        if self.endPointType == 'input':
            endPoint = self.endComponent.inputPoints[self.endPointIndex]
        else:  # output
            endPoint = self.endComponent.outputPoints[self.endPointIndex]

        drawLine(startPoint[0], startPoint[1], endPoint[0], endPoint[1],
                 fill=self.color, lineWidth=2)

        

# ---- EXPRESSION SCREEN ----

def expression_redrawAll(app):
        drawRect(0,0,app.width,app.height, fill = 'gold')
        drawLabel("EXPRESSION",app.width/2, 75, size = 30, fill = 'teal', font = 'Times', bold = True)
        app.backButton.draw()
        drawExpression(200,200, app.expressionText)

def expression_onMousePress(app,mouseX,mouseY):
    if app.backButton.isClicked(mouseX,mouseY):
        setActiveScreen('main')

def drawExpression(x,y,expression):
    # this is the function that draws the expression screen.
    # if there is an error, font is red
    # if expression computed, font is orange
    # computed label should be printed
    if "Error" in expression:
        drawLabel(expression, x, y, size = 24, font = 'Times', fill= 'red', align = 'left')
    else:
        drawLabel(expression, x, y, size = 24, font = 'Times', fill= 'orangeRed', align = 'left')

def generateExpression(app):
    #traverses through the components and generates the final expression text
    # recursive main function
    app.expressions = {}
    app.visited = set()
    finalExprs = []
    for component in app.graphComponents:
        if isinstance(component, Output):
            expr = generateExpressionHelper(component, app.visited, app.expressions, app)
            if expr is None:
                finalExprs.append("Error: undefined component.")
            else:
                finalExprs.append(expr)
    return '\n'.join(finalExprs) if finalExprs else "No Output."

def generateExpressionHelper(component, visited, expressions, app = app):
    # helper function for recursive approach to generateExpression.
    if component in visited:
        return None
    if component in expressions:
        return expressions[component]

    visited.add(component)
    expr = None

    if isinstance(component, Input):
        expr = component.getLabel()

    elif isinstance(component, Output):
        inputExprs = []
        for inputComp in component.connections['inputs']:
            inputExpr = generateExpressionHelper(inputComp, visited, expressions, app)
            if inputExpr is None:
                return None
            inputExprs.append(inputExpr)
        if inputExprs:
            expr = ' AND '.join(inputExprs)
        else:
            expr = 'Output = Undefined'

    elif isinstance(component, Adder):
        inputExprs = []
        for inputComp in component.connections['inputs']:
            inputExpr = generateExpressionHelper(inputComp, visited, expressions, app)
            if inputExpr is None:
                return None
            inputExprs.append(inputExpr)
        if len(inputExprs) == 2:
            sumExpr = f'Sum = ({inputExprs[0]} XOR {inputExprs[1]})'
            carryExpr = f'Carry = ({inputExprs[0]} AND {inputExprs[1]})'
            expr = f'Adder: {sumExpr}; {carryExpr}'
        else:
            expr = 'Sum/Carry = Undefined'

    elif isinstance(component, AndGate):
        inputExprs = []
        for inputComp in component.connections['inputs']:
            inputExpr = generateExpressionHelper(inputComp, visited, expressions, app)
            if inputExpr is None:
                return None
            inputExprs.append(inputExpr)
        expr = f'({" AND ".join(inputExprs)})'

    elif isinstance(component, OrGate):
        inputExprs = []
        for inputComp in component.connections['inputs']:
            inputExpr = generateExpressionHelper(inputComp, visited, expressions, app)
            if inputExpr is None:
                return None
            inputExprs.append(inputExpr)
        expr = f'({" OR ".join(inputExprs)})'

    elif isinstance(component, NotGate):
        if component.connections['inputs']:
            inputExpr = generateExpressionHelper(component.connections['inputs'][0], visited, expressions, app)
            if inputExpr is None:
                return None
            expr = f'NOT({inputExpr})'
        else:
            expr = 'NOT(Undefined)'

    elif isinstance(component, XorGate):
        inputExprs = []
        for inputComp in component.connections['inputs']:
            inpExpr = generateExpressionHelper(inputComp, visited, expressions, app)
            if inpExpr is None:
                return None
            inputExprs.append(inpExpr)
        expr = f"({' XOR '.join(inputExprs)})"

    elif isinstance(component, Node):
        if component.connections['inputs']:
            inputExpr = generateExpressionHelper(component.connections['inputs'][0], visited, expressions, app)
            if inputExpr is None:
                return None
            expr = inputExpr
        else:
            expr = 'Undefined'
    else:
        expr = 'Unknown Component'

    expressions[component] = expr
    visited.remove(component)
    return expr

# ---- XOR SCREEN ----


def xor_redrawAll(app):
        drawRect(0,0,app.width,app.height, fill = 'white')
        drawLabel("XOR SCHEMATIC",app.width/2, 75, size = 30, fill = 'black', font = 'Times', bold = True)
        drawImage(app.xorSchematic, app.width/2, app.height/2, align = 'center')
        app.xorBackButton.draw()

def xor_onMousePress(app,mouseX,mouseY):
    if app.xorBackButton.isClicked(mouseX,mouseY):
        setActiveScreen('main')

# ---- ADDER SCREEN ----

def adder_redrawAll(app):
        drawRect(0,0,app.width,app.height, fill = 'white')
        drawLabel("ADDER SCHEMATIC",app.width/2, 75, size = 30, fill = 'black', font = 'Times', bold = True)
        drawImage(app.adderSchematic, app.width/2, app.height/2, align = 'center')
        app.adderBackButton.draw()

def adder_onMousePress(app,mouseX,mouseY):
    if app.adderBackButton.isClicked(mouseX,mouseY):
        setActiveScreen('main')

# ---- OUTPUT ERROR SCREEN ----

def outputError_redrawAll(app):
        drawRect(0,0,app.width,app.height, fill = 'lightPink')
        drawLabel("MULTIPLE OUTPUT ERROR",app.width/2, 75, size = 60, fill = 'deepPink', font = 'Times', bold = True)
        drawLabel("You can only use one output for the schematic.", app.width/2, 300, size = 48, fill = 'hotPink', font = 'Times')
        drawLabel("I apologize for any inconveniences :(", app.width/2, 350, size = 48, fill = 'hotPink', font = 'Times')
        drawLabel("I hope you still have a fun time building those schematics!", app.width/2, 400, size = 48, fill = 'hotPink', font = 'Times')
        app.outputErrorBackButton.draw()

def outputError_onMousePress(app,mouseX,mouseY):
    if app.outputErrorBackButton.isClicked(mouseX,mouseY):
        setActiveScreen('main')

#back button
class BackButton:
    def __init__(self,x,y, width, height, color, fontColor): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.fontColor = fontColor

    def draw(self):
        # this function draws the back button based on the colors passed through
        drawRect(self.x, self.y, self.width, self.height, fill = self.color,
                 border = self.fontColor, borderWidth = 5, align = 'center')
        drawLabel("BACK", self.x, self.y, size = 24, bold = True, font = 'Times', fill = self.fontColor)


    def isClicked(self, mouseX, mouseY):
        # this function returns a boolean value
        # whether or not mouse is on component
        return self.x - self.width / 2 <= mouseX <= self.x + self.width / 2 and \
               self.y - self.height / 2 <= mouseY <= self.y + self.height / 2

# ---- CMU Graphics ----
def main():
    runAppWithScreens(width=1500, height=1200, initialScreen='start')

main()
