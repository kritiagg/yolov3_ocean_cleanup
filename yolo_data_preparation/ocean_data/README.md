- `filter_acceptable_boxes`: set of helpers to condense data from zooverse 
    - Handles multiple tags of one object by multiple people (if multiple people tagged one picture)
    - Filters out boxes for which a previous user (who tagged the same photo) added a box with IoU > 0.5 (large intersection) or IoSmaler > 0.9 (one is completely within the other)
    - Filters out too big / too small boxes
    - Filters out boxes by blacklisted users
    - Has facilites (not active ATM) to filter out all boxes that haven't been confirmed by another user (i.e. for which there's no box by another user with >.9 IoSmaller or >0.5 IoU)