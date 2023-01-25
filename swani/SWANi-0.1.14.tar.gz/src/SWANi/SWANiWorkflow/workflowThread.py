from PySide6.QtCore import Signal, QObject, QRunnable

from nipype.pipeline import plugins
from logging import Handler, Formatter
from nipype import logging,config
import re, os
import multiprocessing as mp
from threading import Thread

from SWANi.SWANiWorkflow.mainWorkflow import SWANi_wf

from nipype.external.cloghandler import ConcurrentRotatingFileHandler as RFHandler



class gen_SWANi_Signaler(QObject):
        wf = Signal(object)

class gen_SWANi_wf_worker(QRunnable):

    def __init__(self, ptFolder, parent = None):
        super(gen_SWANi_wf_worker,self).__init__(parent)
        self.signal=gen_SWANi_Signaler()
        self.ptFolder=ptFolder

    def run(self):
        self.wf=SWANi_wf(name=os.path.basename(self.ptFolder)+"_nipype",base_dir=self.ptFolder)
        self.signal.wf.emit(self.wf)

class SWANi_wf_process(mp.Process):
    
    NODESTARTED="nodestarted"
    COMPLETED="completed"
    ERROR="error"
    
    def __init__(self, ptName, wf, pipeSender):
        super(SWANi_wf_process,self).__init__()
        self.stopEvent = mp.Event()
        self.wf=wf
        self.pipeSender=pipeSender
        self.ptName=ptName
        
    def wf_run_worker(self,wf, stopEvent):
        plugin_args={'mp_context' : 'fork'}
        if wf.max_cpu>0:
            plugin_args['n_procs']=wf.max_cpu
        wf.run(plugin='MultiProc',plugin_args=plugin_args)
        stopEvent.set()
        
    def run(self):    
        #gestione del file di log nella cartella del paziente
        logdir=os.path.join(self.wf.base_dir,"log/")
        if not os.path.exists(logdir):
             os.mkdir(logdir)
             
        self.wf.config["execution"]["crashdump_dir"] = logdir
        LOG_FILENAME = os.path.join(logdir, "pypeline.log")
        hdlr = RFHandler(
            LOG_FILENAME,
            maxBytes=int(config.get("logging", "log_size")),
            backupCount=int(config.get("logging", "log_rotate")),
        )
        formatter = Formatter(fmt=logging.fmt, datefmt=logging.datefmt)
        hdlr.setFormatter(formatter)
        logging.getLogger("nipype.workflow").addHandler(hdlr)
        logging.getLogger("nipype.utils").addHandler(hdlr)
        logging.getLogger("nipype.filemanip").addHandler(hdlr)
        logging.getLogger("nipype.interface").addHandler(hdlr)
        
        #inizializzo il logger handler
        self.loggerHandler = nipypeLoggerHandler(self.ptName, self.pipeSender)
        logging.getLogger("nipype.workflow").addHandler(self.loggerHandler)
        
        #avvio il wf in un subhread
        wf_run_work = Thread(target=self.wf_run_worker, args=(self.wf,self.stopEvent))
        wf_run_work.start()

        #l'evento può essere settato dal wf_run_worker (se il wf finisce spontaneamente) o dall'esterno per terminare il processo
        self.stopEvent.wait()
        
        #rimuovo gli handler di filelog e aggiornamento gui
        logging.getLogger("nipype.workflow").removeHandler(self.loggerHandler)
        logging.getLogger("nipype.workflow").removeHandler(hdlr)
        logging.getLogger("nipype.utils").removeHandler(hdlr)
        logging.getLogger("nipype.filemanip").removeHandler(hdlr)
        logging.getLogger("nipype.interface").removeHandler(hdlr)
        
        #chiudo la pipe del subprocess
        self.pipeSender.send(logReceiver_worker.STOP)
        self.pipeSender.close()
        
        #se il thread è alive vuol dire che devo killare su richiesta della GUI
        if wf_run_work.is_alive():
            self.kill_with_subprocess()
            
    def kill_with_subprocess(self):
        import psutil
        try:
            thisProcess = psutil.Process(os.getpid())
            children = thisProcess.children(recursive=True)
            
            for process in children:
                process.kill()
            thisProcess.kill()
        except psutil.NoSuchProcess:
            return
        
     
class nipypeLoggerHandler(Handler):
    REG_LOOP=[['Completed \((.*?)\)',SWANi_wf_process.COMPLETED],
            ['Cached \((.*?)\)',SWANi_wf_process.COMPLETED],
            ['\[SWANmonitor\] Error on \"(.*?)\"',SWANi_wf_process.ERROR],
            ['\[SWANmonitor\] Running \"(.*?)\"',SWANi_wf_process.NODESTARTED]]


    def __init__(self, ptName, pipeSender):
        super(nipypeLoggerHandler, self).__init__()
        self.ptName=ptName
        self.pipeSender=pipeSender

    def emit(self, logRecord):
        msg = self.format(logRecord)

        if not self.ptName+"_nipype" in msg:
            return

        for entry in nipypeLoggerHandler.REG_LOOP:
            check=re.search(entry[0],msg)
            if check:
                self.pipeSender.send(check.group(1)+"."+entry[1])
                break


class logReceiver_signal(QObject):
        log_msg = Signal(str)

class logReceiver_worker(QRunnable): 
    STOP="stopstring"

    def __init__(self, pipeReceiver, parent = None):
        super(logReceiver_worker,self).__init__(parent)
        self.signal=logReceiver_signal()
        self.pipeReceiver=pipeReceiver

    def run(self):
        while True:
            # get a unit of work
            item = self.pipeReceiver.recv()
            # check for stop            
            if item==logReceiver_worker.STOP:
                break
            # report
            self.signal.log_msg.emit(item)

orig_report=plugins.base.DistributedPluginBase._report_crash
def _report_crash(self, node, result=None):
    logger = logging.getLogger("nipype.workflow")
    logger.warning('[SWANmonitor] Error on "%s"', node.fullname)
    return orig_report(self, node, result)

orig_sub=plugins.multiproc.MultiProcPlugin._submit_job
def _submit_job(self, node, updatehash=False):
    logger = logging.getLogger("nipype.workflow")
    logger.warning('[SWANmonitor] Running "%s"', node.fullname)
    return orig_sub(self, node, updatehash)

orig_submit_mapnode=plugins.base.DistributedPluginBase._submit_mapnode
def _submit_mapnode(self, jobid):
    logger = logging.getLogger("nipype.workflow")
    logger.warning('[SWANmonitor] Running "%s"', self.procs[jobid].fullname)
    return orig_submit_mapnode(self, jobid)

#Sovrascrivo alcune funzioni di nipype per il monitor eventi
setattr(plugins.base.DistributedPluginBase,"_report_crash",_report_crash)
#SUBMITJOB VIENE ESEGUITO NEL THREAD PRINCIPALE, QUINDI IL SEGNALE PUò ESSERE INVIATO ALLA GUI
setattr(plugins.multiproc.MultiProcPlugin,"_submit_job",_submit_job)
#INIZIO ESECUZIONE MAPNODE
setattr(plugins.base.DistributedPluginBase,"_submit_mapnode",_submit_mapnode)