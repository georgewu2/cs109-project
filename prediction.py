def prediction(array1, array2):
    tracker = 0
    
    if (array1[0] > array2[0]):
        temp = array1
        array1 = array2
        array2 = temp
        tracker = 1
    
    entry = pd.DataFrame(index=range(0, 1), columns=categ)
    merge = array1 + array2 + ['N']
    entry.loc[0]  = merge
    pairings_test = create_pairs(entry)
    test_data = create_prob(pairings_test, trim_lookup2, position_pairs, len(entry))
    X_test = test_data.as_matrix()
    

    predicted = forest_train.predict(X_test)
    if (((list(predicted)[0] == 1) & (tracker ==0)) | ((list(predicted)[0] == 0) & (tracker ==1))):
        print 'Prediction Results: Team 1 Wins'
        return 1
    else:
        print 'Prediction Results: Team 2 Wins'
        return 2