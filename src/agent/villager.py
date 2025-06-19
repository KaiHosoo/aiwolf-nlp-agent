"""村人のエージェントクラスを定義するモジュール."""

from __future__ import annotations

from aiwolf_nlp_common.packet import Role

from agent.agent import Agent


class Villager(Agent):
    """村人のエージェントクラス."""

    def __init__(
        self,
        config: dict,
        name: str,
        game_id: str,
        role: Role,  # noqa: ARG002
    ) -> None:
        """村人のエージェントを初期化する."""
        super().__init__(config, name, game_id, Role.VILLAGER)

    def talk(self) -> str:
        """トークリクエストに対する応答を返す."""
        # プロンプトの読み込み
        with open("./src/agent/talk_prompt.txt", "r", encoding="utf-8") as f:
            prompt = f.read()
        # プロンプトテンプレート中のプレースホルダの置換
        prompt = prompt.replace("{agent_name}", self.agent_name)
        prompt = prompt.replace("{role}", "村人")
        prompt = prompt.replace("{profile}", self.agent_profile)
        prompt = prompt.replace("{day}", str(self.info.day))
        prompt = prompt.replace("{alive_agents}", ",".join(self.get_alive_agents()))
        for t in self.talk_history:
            if t.day != self.info.day: # 異なる日付のトークは無視
                continue
        prompt += f"¥n{t.agent}: {t.text}"
        prompt += f"¥n{self.agent_name}: "
        print(f"Prompt: {prompt}")

        # Google Gemini APIを使用して応答を生成
        # Rate Limit対策のため,他のモデルも併用することがおすすめ
        response = self.gemini.models.generate_content(
            model="gemini-2.0-flash-lite",contents=prompt,
        )
        print(f"Response: {response}")
        return response.text.strip()

    def vote(self) -> str:
        """投票リクエストに対する応答を返す."""
        return super().vote()
