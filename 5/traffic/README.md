load_data():
  - no issues at all, until ddb mentioned that I needed to normalize all values to [0..1]


get_model():

  - changes 1
    - start with dense layer with 128 units
    - adding a dense layer with 64 units improved accuracy by .02 and loss by .02
    - adding a dense layer with 96 units improved accuracy another .02 and loss by .015
    - adding a dense layer with 108 units improved accuracy another .002 and loss by .005

  - changes 2
    - start with dense layer with 256 units: accuracy: 0.9464 - loss: 0.1731

  - changes 3
    - start with dense layer with 512 units: accuracy: 0.9676 - loss: 0.1141

  - changes 4
    - start with dense layer with 384 units: accuracy: 0.9694 - loss: 0.1045
    - adding a dense layer with 64 units: accuracy: 0.9520 - loss: 0.1512

  - changes 5
    - start with dense layer with 320 units: accuracy: 0.9584 - loss: 0.1310
    - adding a dense layer with 64 units: accuracy: 0.9483 - loss: 0.1542

  - changes 5
    - start with dense layer with 360 units: accuracy: 0.9520 - loss: 0.1512
    - set drop out layer to .25: accuracy: 0.9868 - loss: 0.0561
    - set drop out layer to .1: accuracy: 0.9891 - loss: 0.0404
    - set drop out layer to .05: accuracy: 0.9863 - loss: 0.0549


Summary:
For a single dense layer, start out with as many units, topping out around 360 units, to discern as many features as possible as early as possible. Additional layers did not help sufficiently large dense layers. They were only beneficial as additions to dense layers with a low number of units. Low drop out, < .1, was sufficient to fix overfitting from the large number of units.


