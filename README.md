# Immofinder

Small script to find offers on immoscout24.ch by filtering for travel duration to specific locations and keywords.
Please note that this script was created in 2022 for one-time use and later adapted a bit to be configured -> it is rather hacky. Feel free to send a pull request or open an issue if you have propsals etc.

## Usage
Before you can use the script, you need to create a config file named config.json in the same directory as the script. In this file, the location, target location, price range etc. are defined. 
An example configuration can be found in _sample\_config.json_

### Variables

* _location_ is the location for the immoscout search
* _s_ is the type of housing - House is _3_, Appartment is _2_ and _House/Appartment_ is 1
* _t_ is whether you want to buy or rent - _1_ is rent, _2_ is buy
* _priceFrom_, _priceTo_, _roomNumberMin_, _roomNumberMax_ - price range and range of amount of rooms
* _range_ - range in km from _location_ to search
* _searchkeywords_ - keyword that need to be in the offer description (or leave empty)
* _earliestAvailability_ - only show offers that are not available prior to this time.
* _locations_ - set the locations and specify how long the commute from the housing to the specified can take (max value). Max value is specified in _maxDuration_. _maxTravelTime_ is required for the immoscout API.
  * _transportationTypeId_ is to specify if commute is by car, public transport or bicycle. _10_ is for public transport


### Run
Install the requirements: `pip3 install -r requirements.txt`
After you have configured the config file, you can run the script with: `python3 immofinder.py`