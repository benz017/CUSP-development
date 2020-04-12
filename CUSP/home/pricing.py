
def discount_calculator(last_obj):
    disc = last_obj.earlybird_discount
    solo = last_obj.solo_price
    duet = last_obj.duet_price
    tribe = last_obj.tribe_price
    solo = int(solo-(solo*disc)/100)
    duet = int(duet-(duet*disc)/100)
    tribe = int(tribe-(tribe * disc)/100)
    return solo, duet, tribe

