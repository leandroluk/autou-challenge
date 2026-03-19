"use client"

import { Badge } from "@/components/atoms/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/atoms/card"
import { CategoryEnum } from "@/domain/email/enums"

export function ResultSection({
  category,
  reply
}: {
  category: CategoryEnum
  reply: string
}) {
  const isProductive = category === CategoryEnum.PRODUCTIVE

  return (
    <Card className="mt-3 animate-in fade-in slide-in-from-top-4 duration-500 ring-0 shadow-none *:px-0">
      <CardHeader className="flex flex-row items-center justify-between space-y-0">
        <CardTitle className="text-sm font-medium">
          Category
        </CardTitle>
        <Badge variant={isProductive ? "default" : "destructive"}>
          {isProductive ? "Productive" : "Unproductive"}
        </Badge>
      </CardHeader>

      <CardContent className="space-y-3">
        <h3 className="text-xs font-medium text-muted-foreground">Suggested Reply</h3>
        <pre className="text-xs rounded-lg bg-muted p-4 leading-relaxed dark:bg-zinc-900/50 text-justify whitespace-pre-wrap break-words">
          {reply}
        </pre>
      </CardContent>
    </Card>
  )
}