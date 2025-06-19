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

        # Day1とDay2の占い結果を保存するためのインスタンス変数
        self.day1_divine_result = None
        self.day2_divine_result = None


    def talk(self) -> str:
        """トークリクエストに対する応答を返す."""
        if self.info.divine_result is not None:
            if self.info.day == 1 and self.day1_divine_result is None:
                # Day1の占い結果がまだない場合、Day1の占い結果を保存
                self.day1_divine_result = self.info.divine_result
            elif self.info.day == 2 and self.day2_divine_result is None:
                # Day2の占い結果がまだない場合、Day2の占い結果を保存
                self.day2_divine_result = self.info.divine_result
            else:
                # 報告済みの場合 or 占い結果がない場合は何もしない
                return "Over"

            # 占い結果を報告していない場合は報告する
            if self.info.divine_result.result == "HUMAN":
                return f"{self.info.divine_result.target}さんは人間でした"
            else:
                return f"{self.info.divine_result.target}さんは人狼でした"
        # 占い結果がない場合はOverを返す
        return "Over"

    def divine(self) -> str:
        alive_agents = self.get_alive_agents()
        alive_agents.remove(self.agent_name)  # 自分自身を除外

        # 1日目の占い済みのエージェントを除外
        if self.day1_divine_result is not None:
            alive_agents.remove(self.day1_divine_result.target)
        # 残っているエージェントから適当に選ぶ
        return alive_agents[0]


    def vote(self) -> str:
        vote_target = None

        alive_agents = self.get_alive_agents()
        alive_agents.remove(self.agent_name)  # 自分自身を除外
        
        # 占い結果が人狼のプレイヤに投票
        if self.day1_divine_result is not None: # 1日目の占い結果がある場合
            if self.day1_divine_result.result == "WEREWOLF":
                # 1日目の占い結果が人狼の場合はそのプレイヤを投票候補にする
                vote_target =  self.day1_divine_result.target
            else:
                # 人間の場合は人間のプレイヤを投票候補から削除
                alive_agents.remove(self.day1_divine_result.target)
        elif self.day2_divine_result is not None: # 2日目の占い結果がある場合
            if self.day2_divine_result.result == "WEREWOLF":
                # 2日目の占い結果が人狼の場合はそのプレイヤを投票候補にする
                vote_target =  self.day2_divine_result.target
            else:
                # 人間の場合は人間のプレイヤを投票候補から削除
                alive_agents.remove(self.day2_divine_result.target)
        if vote_target is None:
            # 占い結果がない場合は適当に生存エージェントを選ぶ
            vote_target = alive_agents[0]
        return vote_target
