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
        print("My name", self.agent_name) # 自分の名前
        print("My profile" , self.agent_profile) # 自分のプロフィール
        print("talk_history", self.talk_history) # 対話履歴
        print("divine results", self.info.divine_result) # 占い結果
        print("alive agents", self.get_alive_agents()) # 生存エージェント
        print("vote_list", self.info.vote_list) # 投票リスト
        print("info", self.info) # 全体の情報
        
        return super().talk()

    def divine(self) -> str:
        """占いリクエストに対する応答を返す."""            
        return super().divine()

    def vote(self) -> str:
        """投票リクエストに対する応答を返す."""
        return super().vote()
