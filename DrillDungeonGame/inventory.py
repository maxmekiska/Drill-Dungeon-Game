class Inventory:
    """

    Contains the inventory of the drill (player).

    """
    def __init__(self, gold: int = 0, coal: int = 0, ammunition: int = 0) -> None:
        """

        Parameters
        ----------
        gold        : int
            Total count of gold collected and available to the player.
        coal        : int
            Total count of coal collectd and available to the player.
        ammunition  : int
            Total amount of bullets available to the player to shoot.

        """
        self.gold = gold
        self.coal = coal
        self.ammunition = ammunition
