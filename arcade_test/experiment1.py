import arcade

window = arcade.Window(title="Arcade tutorials")
window.center_window()


class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__(window, arcade.color.AFRICAN_VIOLET)

        self.batch = arcade.shape_list.ShapeElementList()

        ellipse1 = arcade.shape_list.create_ellipse_filled(
            440, 360, 50, 150, arcade.color.ROSE
        )

        self.batch.append(ellipse1)

    def on_draw(self) -> None:
        self.clear(arcade.color.AIR_SUPERIORITY_BLUE)
        self.batch.draw()

if __name__ == "__main__":
    game = GameView()
    window.show_view(game)
    arcade.run()
