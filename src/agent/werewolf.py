"""人狼のエージェントクラスを定義するモジュール."""

from __future__ import annotations

from aiwolf_nlp_common.packet import Role

from agent.agent import Agent


class Werewolf(Agent):
    """人狼のエージェントクラス."""

    def __init__(
        self,
        config: dict,
        name: str,
        game_id: str,
        role: Role,  # noqa: ARG002
    ) -> None:
        """人狼のエージェントを初期化する."""
        super().__init__(config, name, game_id, Role.WEREWOLF)

    def whisper(self) -> str:
        """囁きリクエストに対する応答を返す."""
        return super().whisper()

    def talk(self) -> str:
        """トークリクエストに対する応答を返す."""
        #return super().talk()
        # 村人になりすまし、誰かを疑う発言をする
        suspicious = self.get_most_suspicious()
        if suspicious:
            return f"{suspicious} が怪しいと思います。"
        return "まだよくわかりませんね。"

    def vote(self) -> str:
        """投票リクエストに対する応答を返す."""
        return super().vote()

    def attack(self) -> str:
        """襲撃リクエストに対する応答を返す."""
        #return super().attack()
        # 自分以外の生存者からランダムに選んで襲撃
        targets = [a for a in self.get_alive_agents() if a != self.agent_name]
        return targets[0] if targets else self.agent_name
