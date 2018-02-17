# -*- coding: utf-8 -*-


class JsonExporter(object):

    @staticmethod
    def export_player(player):
        """
        Let's export tiles in 34 tile format.
        It will allow to build more clear predictions.
        """

        discards = []
        for discard in player.discards:
            discards.append({
                'tile': to_34(discard.tile),
            })

        melds = []
        for meld in player.melds:
            melds.append({
                'type': meld.type,
                'tiles': [to_34(x) for x in meld.tiles]
            })

        data = {
            'log_id': player.table.log_id,
            'player_seat': player.seat,
            'hand_number': player.table.current_hand,
            'player_hand': sorted([to_34(x) for x in player.tiles]),
            'discards': discards,
            'melds': melds,
            'waiting': player.waiting,
        }

        return data


def to_34(tile):
    return tile // 4
