import sys

indentSpaces = ''

def checkFileName(filename):
    global file
    if '.' not in filename:
        filename += '.pys'
    elif filename[-4] != '.':
        filename = filename.replace('.', '') + '.pys'
    elif not filename.endswith('.pys'):
        filename = filename.split('.')[0] + '.pys'
    file = open(filename, 'r')

def removeIndents(string):
    indentLevel = 0
    while True:
        string = string.lstrip(indentSpaces)
        indentLevel += 1
        if not string.startswith(' '):
            break
    return string, indentLevel

def interpret():
    finalCode = ''
    commented = False
    for line in file:
        ignoreLine = False
        updatedLine = line.strip('\n').rstrip().split('//')[0].rstrip()
        updatedLine = updatedLine.replace('null', 'None')
        updatedLine = updatedLine.replace('true', 'True')
        updatedLine = updatedLine.replace('false', 'False')
        updatedLine = updatedLine.replace('func', 'def')
        if removeIndents(updatedLine)[0].startswith('if') or removeIndents(updatedLine)[0].startswith('while') or removeIndents(updatedLine)[0].startswith('for') or removeIndents(updatedLine)[0].startswith('elif') or removeIndents(updatedLine)[0].startswith('} elif'):
            updatedLine = updatedLine.replace(') {', ':', 1)
            updatedLine = updatedLine.replace('(', '', 1)
        elif removeIndents(updatedLine)[0].startswith('def') or removeIndents(updatedLine)[0].startswith('else') or removeIndents(updatedLine)[0].startswith('} else') or removeIndents(updatedLine)[0].startswith('try'):
            updatedLine = updatedLine.replace(' {', ':', 1)
        if removeIndents(updatedLine)[0].startswith('}'):
            if removeIndents(updatedLine)[0] == '}':
                ignoreLine = True
            else: updatedLine = updatedLine.replace('} ', '', 1)
        updatedLine = updatedLine.replace('//', '#')
        if commented:
            updatedLine = '# ' + updatedLine
        if '/*' in updatedLine:
            updatedLine = updatedLine.replace('/*', '#')
            commented = True
        if '*/' in updatedLine:
            updatedLine = updatedLine.replace('*/', '')
            commented = False
        if 'PYS' in updatedLine:
            print('importing PYS essentials')
            # import essentials as PYS
            finalCode = 'import essentials as PYS\n\n' + finalCode
        if not ignoreLine:
            try:
                finalCode += '\n' + updatedLine + ' # ' + line.strip('\n').rstrip().split('//')[1].lstrip()
            except IndexError as e:
                finalCode += '\n' + updatedLine
    return finalCode

if __name__ == '__main__':
    try:
        checkFileName(sys.argv[1])
    except:
        print("Make sure that you specify a valid filename with the extension '.pys'")
        quit()
    try:
        for _ in range(int(sys.argv[2])):
            indentSpaces += ' '
    except:
        indentSpaces = '    '
    finalCode = interpret()
    print(finalCode)
    print('\nRUNNING\n\n')
    exec(finalCode)