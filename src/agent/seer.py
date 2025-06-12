"""占い師のエージェントクラスを定義するモジュール."""

from __future__ import annotations

from aiwolf_nlp_common.packet import Role

from agent.agent import Agent


class Seer(Agent):
    """占い師のエージェントクラス."""

    def __init__(
        self,
        config: dict,
        name: str,
        game_id: str,
        role: Role,  # noqa: ARG002
    ) -> None:
        """占い師のエージェントを初期化する."""
        super().__init__(config, name, game_id, Role.SEER)

    def talk(self) -> str:
        """トークリクエストに対する応答を返す."""
        day = self.info.day
        turn = self.info.talk_turn

        # デバッグ出力（必要に応じて残す）
        print("My name", self.agent_name)
        print("My profile" , self.agent_profile)
        print("talk_history", self.talk_history)
        print("divine results", self.info.divine_result)
        print("alive agents", self.get_alive_agents())
        print("vote_list", self.info.vote_list)
        print("info", self.info)

        # 0日目は発話しない（プロローグ）
        if day == 0:
            return "Over"

        # その日最初の発話なら、占い結果を報告
        if turn == 0 and self.info.divine_result:
            last_result = self.info.divine_result[-1]
            target = last_result.target.name
            species = "人狼" if last_result.result.name == "WEREWOLF" else "人間"
            return f"{target}さんは{species}でした"

        return "Over"
        #return super().talk()

    def divine(self) -> str:
        """占いリクエストに対する応答を返す."""            
        return super().divine()

    def vote(self) -> str:
        """投票リクエストに対する応答を返す."""
        return super().vote()
