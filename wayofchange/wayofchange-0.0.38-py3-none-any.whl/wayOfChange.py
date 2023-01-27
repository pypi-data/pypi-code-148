'''from classFiles.JazzNote import JazzNote
from classFiles.Change import Change
from classFiles.Utility import Utility'''
from Utility import Utility
from JazzNote import JazzNote
from Change import Change
from Graphics import Graphics
from tqdm import tqdm
from pprint import pprint

#from pprint import pprint
import random, math
input = Utility.input
print = Utility.print
change = Change(['1','5'])
#print(change.byWays(['Word']))
notWorkingWays = []
def testWays():
    ret = {}
    result = ''
    notWorkingWays = {}
    for i in range(1361,1362):
        print('in testWays, i =',i)
        change = Change.makeFromChangeNumber(i)

        #input(i, change, change.byWays('Carnatic'))
        ways = [way for way in Change.validWays if "Poem" not in way]
        #random.seed(50)
        #random.shuffle(ways)

        for w,way in tqdm(enumerate(ways)):


            print('top of way loop')
            _result = ''
            try:
                #print(w, way, end='----->   ')
                _result += '{} {} -> '.format(w, way)
                changeByWay = change.byWays([way])
                if type(changeByWay) in (Change, list, tuple):
                    changeByWay = ', '.join([str(v) for v in changeByWay])
                _result += '{}\n'.format(changeByWay)
                #print(changeByWay,end='')
            except Exception as e:
                _result = ''
                _result += '\t# {} {} \t\t\t{}\n'.format(w,way,e)
                #print('\t#',w,way,end=', ')
                notWorkingWays[way] = w
                #print('\t!!!!Not Yet Working!!!!')
            result += _result
            #print()
            print('doing',w,way)

    non_working_result = '\nNon working ways num = {}\n {}\n'.format(len(notWorkingWays),', '.join( [ str(i) for i in notWorkingWays]))
    result = non_working_result + result + non_working_result

    ret['result'] = result
    ret['notWorkingWays'] = notWorkingWays

    try:
        change:Change
        ret['nextBadWay'] = change.byWays([list(notWorkingWays.keys())[0]])

    except IndexError:
        ret['nextBadWay'] = None
    pprint(ret)

    return ret

if __name__ == '__main__':
    print('passing testWays()...')
    pprint(testWays())
    print('done passing testWays()')
    print('done executing succesfully')