
xctWorkManagerList = [
    [ 'WMBPELInvoker', '1', '8' ],
    [ 'WMOutgoingInitiation', '1', '1' ],
    [ 'WMNotification', '1', '1' ],
    [ 'WMParser', '1', '4' ],
    [ 'WMInterfacingReply', '1', '1' ],
    [ 'WMInterfacingHerald', '1', '1' ],
    [ 'WMInterfacingRequest', '1', '1' ],
    [ 'WMInterchangeLoader', '1', '2' ],
    [ 'WMDataImport', '1', '1' ],
    [ 'WMUrgency8InterchangeLoader', '1', '2' ],
    [ 'WMUrgency8Parser', '1', '4' ],
    [ 'WMUrgency8BPELInvoker', '1', '8' ],
    [ 'WMTransportReceipt', '1', '1' ],
    [ 'WMSOInitiation', '1', '1' ],
    [ 'WMChannel', '1', '1' ],
    [ 'WMSwiftInterchangeLoader', '1', '2' ],
    [ 'WMBilling', '1', '1' ],
    [ 'WMForexService', '1', '1' ],
    [ 'WMReconciliationTimeout', '1', '1' ],
    [ 'WMGPIEndOfDayConfirmationService', '1', '1' ],
    [ 'WMGPIEndOfDayConfirmationCandidateService', '1', '1' ]
]



for wm in xctWorkManagerList:
    workManagerName = wm[0]
    maxThreadConstraintName = workManagerName + '-max'
    minThreadConstraintName = workManagerName + '-min'
    MinThread = wm[1]
    MaxThread = wm[2]
    edit()
    startEdit()
    print '======= Creating a WorkManager name as ======='
    cd('edit:/SelfTuning/' + domainName + '/WorkManagers/')
    create(workManagerName,'WorkManagers')
    cd('edit:/SelfTuning/' + domainName + '/WorkManagers/' + workManagerName)
    cmo.addTarget(getMBean("/Servers/"+ targetServer))
    save()
    print ' WorkManager Created...'    
    print '======= Creating MaxThreadsConstraint ======='
    cd('edit:/SelfTuning/' + domainName + '/MaxThreadsConstraints/')
    try:
        create(maxThreadConstraintName,'MaxThreadsConstraints')
    except Exception:
        print 'Issue in Creating MaxThreads exiting'
    cd('edit:/SelfTuning/' + domainName + '/MaxThreadsConstraints/' + maxThreadConstraintName)
    cmo.addTarget(getMBean("/Servers/"+ targetServer))
    set('Count',MaxThread)
    save()   
    print '======= Creating MinThreadsConstraint ======='
    cd('edit:/SelfTuning/' + domainName + '/MinThreadsConstraints/')
    try:
        create(minThreadConstraintName,'MinThreadsConstraints')
    except Exception:
        print 'Issue In Creating MinThreads '
    cd('edit:/SelfTuning/' + domainName + '/MinThreadsConstraints/' + minThreadConstraintName)
    cmo.addTarget(getMBean("/Servers/"+ targetServer))
    set('Count',MinThread)
    save()  
    print '======= Assigning the MaxThreadConstraint to the WorkManager ======='
    cd('edit:/SelfTuning/' + domainName + '/WorkManagers/' + workManagerName)
    bean=getMBean('/SelfTuning/' + domainName + '/MaxThreadsConstraints/' + maxThreadConstraintName)
    cmo.setMaxThreadsConstraint(bean)    
    print '======= Assigning the MinThreadConstraint to the WorkManager ======='
    cd('edit:/SelfTuning/' + domainName + '/WorkManagers/' + workManagerName)
    bean=getMBean('/SelfTuning/' + domainName + '/MinThreadsConstraints/' + minThreadConstraintName)
    cmo.setMinThreadsConstraint(bean)   
    save()
    #activate(block="true")
print '==> WorkManager Creation Finished ... Please Double Check from AdminConsole...'