def predict_with_decision_tree(feature_vector):
  """DecisionTreeModel classifier of depth 5 with 37 nodes"""

  if feature_vector[0] <= 0.23874:
    if feature_vector[1] <= 7.2797:
      if feature_vector[0] <= -0.36279:
        if feature_vector[2] <= 6.6779:
          if feature_vector[1] <= 5.496:
            return 1.0
          else:
            return 1.0
        else:
          if feature_vector[1] <= -4.6145:
            return 1.0
          else:
            return 0.0
      else:
        if feature_vector[2] <= 2.3586:
          if feature_vector[1] <= 4.1986:
            return 1.0
          else:
            return 0.0
        else:
          return 0.0
    else:
      if feature_vector[0] <= -3.9172:
        if feature_vector[2] <= 0.61663:
          return 1.0
        else:
          return 0.0
      else:
        return 0.0
  else:
    if feature_vector[2] <= -4.4738:
      if feature_vector[0] <= 2.5227:
        return 1.0
      else:
        return 0.0
    else:
      if feature_vector[0] <= 1.5514:
        if feature_vector[2] <= -1.6283:
          if feature_vector[1] <= 3.6957:
            return 1.0
          else:
            return 0.0
        else:
          if feature_vector[3] <= 0.84998:
            return 0.0
          else:
            return 1.0
      else:
        if feature_vector[0] <= 2.1721:
          if feature_vector[2] <= -1.6283:
            return 1.0
          else:
            return 0.0
        else:
          return 0.0
print predict_with_decision_tree([-0.3579, 9.496, 6.5779, 2.0])
